from libqtile import widget


class MyVolume(widget.Volume):
    """
    PulseAudio volume widget using `pactl`.
    Doesn't rely on additional dependencies unlike the built in `PulseVolume` widget.

    Mouse callbacks inherited from widget.Volume:
    - Button1: mute
    - Button3: run volume_app
    - Button4: increase volume
    - Button5: decrease volume
    """

    def __init__(self, **kwargs):
        volume_control = "~/.config/qtile/scripts/volume-control.sh"
        kwargs.setdefault("get_volume_command", "pactl get-sink-volume @DEFAULT_SINK@")
        kwargs.setdefault("check_mute_command", "pactl get-sink-mute @DEFAULT_SINK@")
        kwargs.setdefault("check_mute_string", "yes")
        kwargs.setdefault("mute_command", f"{volume_control} mute")
        kwargs.setdefault("volume_up_command", f"{volume_control} up 5")
        kwargs.setdefault("volume_down_command", f"{volume_control} down 5")
        kwargs.setdefault("volume_app", "pavucontrol")
        super().__init__(**kwargs)

    def _update_drawer(self):
        if not self.theme_path or self.emoji:
            if self.is_mute or self.volume == -1:
                self.text = "MUTE"
            elif self.volume == 100:
                self.text = "FULL"
            elif self.volume < 10:
                # Add leading whitespace to always have a two character length.
                self.text = f" {self.volume} %"
            else:
                self.text = f"{self.volume} %"
