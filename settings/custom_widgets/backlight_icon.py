# Copyright (c) 2012 Tim Neumann
# Copyright (c) 2012, 2014 Tycho Andersen
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2014 Sean Vig
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import widget


class MyBacklightIcon(widget.Backlight):
    """
    Child class to format the percentage output.

    Note: the "format" kwarg needs to be set to "{percent}" for the widget to display
    the correct value.
    """

    def __init__(self, icon, low_color, min_color, max_color, **kwargs):
        self.icon = icon
        self.low_color = low_color
        self.min_color = min_color
        self.max_color = max_color
        super().__init__(**kwargs)

    def _get_info(self):
        brightness = self._load_file(self.brightness_file)
        max_value = self._load_file(self.max_brightness_file)
        return int((brightness / max_value) * 100)

    def poll(self):
        try:
            percent = self._get_info()
        except RuntimeError as e:
            return "Error: {}".format(e)

        return percent

    def tick(self):
        current_brightness = self.poll()

        if current_brightness <= 0:
            text = f"<span foreground='{self.low_color}'>{self.icon}</span>"
        elif current_brightness < 50:
            text = f"<span foreground='{self.min_color}'>{self.icon}</span>"
        else:
            text = f"<span foreground='{self.max_color}'>{self.icon}</span>"

        self.update(text)
