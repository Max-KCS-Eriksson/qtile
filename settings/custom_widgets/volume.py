from libqtile import widget


class MyVolume(widget.Volume):
    """
    Child class to add whitespace in self.text between the numerical volume value and
    the percentage sign.

    http://docs.qtile.org/en/latest/_modules/libqtile/widget/volume.html
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _update_drawer(self):
        if not self.theme_path or self.emoji:
            if self.volume == -1:
                self.text = "MUTE"
            elif self.volume == 100:
                self.text = "FULL"
            elif self.volume < 10:
                # Add leading whitespace to always have a two character length.
                self.text = f" {self.volume} %"
            else:
                self.text = f"{self.volume} %"
