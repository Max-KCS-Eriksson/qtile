from libqtile import widget


class MyVolumeIcon(widget.Volume):
    """
    Changes color according to current volume.

    Takes a string as an argument for the icon, mute_color, min_color, med_color, and
    max_color parameters.

    http://docs.qtile.org/en/latest/_modules/libqtile/widget/volume.html
    """

    def __init__(self, icon, mute_color, min_color, med_color, max_color, **kwargs):
        self.icon = icon
        self.mute_color = mute_color
        self.min_color = min_color
        self.med_color = med_color
        self.max_color = max_color
        super().__init__(**kwargs)

    def _update_drawer(self):
        if not self.theme_path or self.emoji:
            if self.volume == -1:
                self.text = f"<span foreground='{self.mute_color}'>{self.icon}</span>"
            elif self.volume == 100:
                self.text = f"<span foreground='{self.max_color}'>{self.icon}</span>"
            elif self.volume < 10:
                # Add leading whitespace to always have a two character length.
                self.text = f"<span foreground='{self.min_color}'>{self.icon}</span>"
            elif self.volume < 60:
                self.text = f"<span foreground='{self.min_color}'>{self.icon}</span>"
            elif self.volume < 80:
                self.text = f"<span foreground='{self.med_color}'>{self.icon}</span>"
            else:
                self.text = f"<span foreground='{self.max_color}'>{self.icon}</span>"
