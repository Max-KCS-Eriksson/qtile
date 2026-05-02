#!/bin/bash

set -euo pipefail

action="${1:-}"
step="${2:-5}"

unmute() {
    pactl set-sink-mute @DEFAULT_SINK@ false
    amixer -q set Master unmute
}

is_pulse_muted() {
    pactl get-sink-mute @DEFAULT_SINK@ | grep -q "yes"
}

is_master_muted() {
    amixer get Master | grep -q "\[off\]"
}

case "$action" in
    up)
        unmute
        pactl set-sink-volume @DEFAULT_SINK@ +"${step}"%
        ;;
    down)
        unmute
        pactl set-sink-volume @DEFAULT_SINK@ -"${step}"%
        ;;
    mute)
        if is_pulse_muted || is_master_muted; then
            unmute
        else
            pactl set-sink-mute @DEFAULT_SINK@ true
            amixer -q set Master mute
        fi
        ;;
    *)
        echo "Usage: $0 {up|down|mute} [step]" >&2
        exit 2
        ;;
esac
