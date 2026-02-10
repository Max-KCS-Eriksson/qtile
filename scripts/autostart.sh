#!/bin/bash

function run {
    if ! pgrep -x "$(basename "$1" | head -c 15)" 1>/dev/null; then
        "$@" &
    fi
}

if [[ "$(xrandr | grep ' connected' | wc -l)" -gt 1 ]]; then
    xrandr --output eDP-1 --scale 0.7
fi

# Wallpaper

feh --no-fehbg --bg-fill ~/.config/backgrounds/gruvbox_mojave.jpg &
betterlockscreen --update ~/Pictures/memes/bun_don_babylon_penguin_shadow_darker.jpg &

# Start sxhkd to replace Qtile native key-bindings

run sxhkd -c ~/.config/qtile/sxhkd/sxhkdrc &

# Utility applications

run nm-applet &
blueman-applet &
rfkill block bluetooth &

wezterm &
