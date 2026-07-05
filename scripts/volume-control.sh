#!/bin/bash

set -euo pipefail

action="${1:-}"
step="${2:-5}"
debug="${VOLUME_CONTROL_DEBUG:-0}"
log_file="${VOLUME_CONTROL_LOG:-/tmp/volume-control.log}"
audio_timeout="${VOLUME_CONTROL_TIMEOUT:-2}"

alsa_control="${ALSA_CONTROL:-Master}"
audio_backend_cache=""
runtime_dir="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
pulse_socket="${runtime_dir}/pulse/native"
preferred_pulse_sink_name="${PREFERRED_PULSE_SINK:-}"

if [[ -d "$runtime_dir" ]]; then
    export XDG_RUNTIME_DIR="$runtime_dir"
fi

if [[ -z "${PULSE_SERVER:-}" && -S "$pulse_socket" ]]; then
    export PULSE_SERVER="unix:$pulse_socket"
fi

log() {
    if [[ "$debug" == "1" ]]; then
        printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >>"$log_file"
    fi
}

run_audio() {
    if command -v timeout >/dev/null 2>&1; then
        timeout "${audio_timeout}s" "$@"
    else
        "$@"
    fi
}

pulse_available() {
    if [[ -n "${PULSE_SERVER:-}" || -S "$pulse_socket" ]]; then
        command -v pactl >/dev/null 2>&1 && run_audio pactl info >/dev/null 2>&1
    fi
}

audio_backend() {
    if [[ -n "$audio_backend_cache" ]]; then
        printf '%s\n' "$audio_backend_cache"
        return 0
    fi

    if pulse_available; then
        audio_backend_cache="pulse"
    else
        audio_backend_cache="alsa"
    fi

    printf '%s\n' "$audio_backend_cache"
}

pulse_sink_exists() {
    local sink="$1"

    run_audio pactl list short sinks 2>/dev/null | awk -v sink="$sink" '$2 == sink { found = 1 } END { exit !found }'
}

preferred_pulse_sink() {
    local sink

    if [[ -n "$preferred_pulse_sink_name" ]] && pulse_sink_exists "$preferred_pulse_sink_name"; then
        printf '%s\n' "$preferred_pulse_sink_name"
        return 0
    fi

    sink="$(
        { run_audio pactl list sinks 2>/dev/null || true; } | awk '
            function flush() {
                if (name == "") {
                    return
                }

                haystack = tolower(name " " description " " ports)
                if (preferred == "" && haystack ~ /(speaker|headphones)/ && haystack !~ /(hdmi|displayport)/) {
                    preferred = name
                }
                if (fallback == "" && haystack !~ /(hdmi|displayport)/) {
                    fallback = name
                }

                name = ""
                description = ""
                ports = ""
            }

            /^Sink #/ {
                flush()
                next
            }
            /^[[:space:]]*Name:/ {
                name = $2
                next
            }
            /^[[:space:]]*Description:/ {
                sub(/^[[:space:]]*Description:[[:space:]]*/, "")
                description = $0
                next
            }
            /^[[:space:]]*\[Out\]/ || /^[[:space:]]*Active Port:/ {
                ports = ports " " $0
                next
            }
            END {
                flush()
                if (preferred != "") {
                    print preferred
                } else if (fallback != "") {
                    print fallback
                }
            }
        '
    )"

    if [[ -n "$sink" ]]; then
        printf '%s\n' "$sink"
        return 0
    fi

    run_audio pactl get-default-sink 2>/dev/null
}

move_sink_inputs() {
    local sink="$1"
    local input_id

    while read -r input_id _; do
        [[ -n "$input_id" ]] || continue
        run_audio pactl move-sink-input "$input_id" "$sink" >/dev/null 2>&1 || true
    done < <(run_audio pactl list short sink-inputs 2>/dev/null || true)
}

ensure_preferred_pulse_sink() {
    local sink default_sink

    sink="$(preferred_pulse_sink || true)"
    [[ -n "$sink" ]] || return 1

    default_sink="$(run_audio pactl get-default-sink 2>/dev/null || true)"
    if [[ "$default_sink" != "$sink" ]]; then
        log "switching default sink: ${default_sink:-unknown} -> $sink"
        run_audio pactl set-default-sink "$sink" >/dev/null 2>&1 || true
        move_sink_inputs "$sink"
    fi

    printf '%s\n' "$sink"
}

pulse_volume_percent() {
    local sink="${1:-@DEFAULT_SINK@}"
    local output volume

    output="$(run_audio pactl get-sink-volume "$sink" 2>&1)" || return 1
    volume="$(grep -oE '[0-9]+%' <<<"$output" | head -n1 | tr -d '%')" || return 1
    [[ -n "$volume" ]] || return 1
    printf '%s%%\n' "$volume"
}

alsa_volume_percent() {
    command -v amixer >/dev/null 2>&1 || return 1

    local output volume
    output="$(run_audio amixer get "$alsa_control" 2>&1)" || {
        log "amixer get $alsa_control failed: $output"
        return 1
    }
    log "amixer $alsa_control status: $output"
    volume="$(grep -oE '[0-9]+%' <<<"$output" | head -n1 | tr -d '%')" || return 1
    [[ -n "$volume" ]] || return 1
    printf '%s%%\n' "$volume"
}

dump_state() {
    if [[ "$debug" != "1" ]]; then
        return
    fi

    log "default sink: $(run_audio pactl get-default-sink 2>&1 || true)"
    log "preferred sink: $(preferred_pulse_sink 2>&1 || true)"
    log "sink mute: $(run_audio pactl get-sink-mute @DEFAULT_SINK@ 2>&1 || true)"
    log "sink volume: $(run_audio pactl get-sink-volume @DEFAULT_SINK@ 2>&1 || true)"
    log "amixer scontrols: $(run_audio amixer scontrols 2>&1 || true)"
    log "amixer Master: $(run_audio amixer get Master 2>&1 || true)"
    log "pulse available: $(pulse_available && echo yes || echo no)"
}

is_pulse_muted() {
    local sink="${1:-@DEFAULT_SINK@}"
    local output
    output="$(run_audio pactl get-sink-mute "$sink" 2>&1)" || {
        log "pactl get-sink-mute failed: $output"
        return 1
    }
    log "pactl mute status: $output"
    grep -q "yes" <<<"$output"
}

is_alsa_muted() {
    command -v amixer >/dev/null 2>&1 || return 1

    local output
    output="$(run_audio amixer get "$alsa_control" 2>&1)" || {
        log "amixer get $alsa_control failed: $output"
        return 1
    }
    log "amixer $alsa_control status: $output"
    grep -q "\[off\]" <<<"$output"
}

pulse_unmute() {
    local sink="${1:-@DEFAULT_SINK@}"

    log "pactl unmute sink $sink"
    run_audio pactl set-sink-mute "$sink" false
}

pulse_mute() {
    local sink="${1:-@DEFAULT_SINK@}"

    log "pactl mute sink $sink"
    run_audio pactl set-sink-mute "$sink" true
}

pulse_volume() {
    local sink="${1:-@DEFAULT_SINK@}"

    log "pactl query volume"
    pulse_volume_percent "$sink" || echo "0%"
}

alsa_unmute_all() {
    command -v amixer >/dev/null 2>&1 || return 0

    log "amixer unmute $alsa_control"
    run_audio amixer -q set "$alsa_control" unmute >/dev/null 2>&1 || true
}

alsa_mute_all() {
    command -v amixer >/dev/null 2>&1 || return 0

    log "amixer mute $alsa_control"
    run_audio amixer -q set "$alsa_control" mute >/dev/null 2>&1 || true
}

case "$action" in
    up)
        log "action=up step=$step"
        dump_state
        if [[ "$(audio_backend)" == pulse ]]; then
            sink="$(ensure_preferred_pulse_sink || printf '@DEFAULT_SINK@')"
            pulse_unmute "$sink"
            run_audio pactl set-sink-volume "$sink" +"$step"%
        else
            alsa_unmute_all
            command -v amixer >/dev/null 2>&1 && run_audio amixer -q set "$alsa_control" "${step}%+" >/dev/null 2>&1 || true
        fi
        dump_state
        ;;
    down)
        log "action=down step=$step"
        dump_state
        if [[ "$(audio_backend)" == pulse ]]; then
            sink="$(ensure_preferred_pulse_sink || printf '@DEFAULT_SINK@')"
            pulse_unmute "$sink"
            run_audio pactl set-sink-volume "$sink" -"$step"%
        else
            alsa_unmute_all
            command -v amixer >/dev/null 2>&1 && run_audio amixer -q set "$alsa_control" "${step}%-" >/dev/null 2>&1 || true
        fi
        dump_state
        ;;
    mute)
        log "action=mute"
        dump_state
        if [[ "$(audio_backend)" == pulse ]]; then
            sink="$(ensure_preferred_pulse_sink || printf '@DEFAULT_SINK@')"
            if is_pulse_muted "$sink"; then
                log "muted detected -> unmute"
                pulse_unmute "$sink"
            else
                log "unmuted detected -> mute"
                pulse_mute "$sink"
            fi
        else
            if is_alsa_muted; then
                log "muted detected -> unmute"
                alsa_unmute_all
            else
                log "unmuted detected -> mute"
                alsa_mute_all
            fi
        fi
        dump_state
        ;;
    status)
        log "action=status"
        dump_state
        if [[ "$(audio_backend)" == pulse ]]; then
            sink="$(ensure_preferred_pulse_sink || printf '@DEFAULT_SINK@')"
            if is_pulse_muted "$sink"; then
                log "status=yes"
                echo yes
            else
                log "status=no"
                echo no
            fi
        elif is_alsa_muted; then
            log "status=yes"
            echo yes
        else
            log "status=no"
            echo no
        fi
        ;;
    volume)
        log "action=volume"
        dump_state
        if [[ "$(audio_backend)" == pulse ]]; then
            sink="$(ensure_preferred_pulse_sink || printf '@DEFAULT_SINK@')"
            pulse_volume "$sink"
        else
            alsa_volume_percent || echo "0%"
        fi
        ;;
    *)
        echo "Usage: $0 {up|down|mute|status|volume} [step]" >&2
        exit 2
        ;;
esac
