from libqtile import widget


class MyBacklight(widget.Backlight):
    """
    Child class to format the percentage output.

    Note: the "format" kwarg needs to be set to "{percent}" for the widget to display
    the correct value.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_info(self):
        brightness = self._load_file(self.brightness_file)
        max_value = self._load_file(self.max_brightness_file)
        current_brightness = int((brightness / max_value) * 100)

        if current_brightness <= 0:
            return "DARK"
        elif current_brightness == 100:
            return "FULL"
        elif current_brightness < 10:
            return f" {current_brightness} %"
        else:
            return f"{current_brightness} %"
