# Copyright (c) 2008, 2010 Aldo Cortesi
# Copyright (c) 2009 Ben Duffield
# Copyright (c) 2010 aldo
# Copyright (c) 2010-2012 roger
# Copyright (c) 2011 Florian Mounier
# Copyright (c) 2011 Kenji_Takahashi
# Copyright (c) 2011-2015 Tycho Andersen
# Copyright (c) 2012-2013 dequis
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 xarvh
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2014 Sean Vig
# Copyright (c) 2014 Filipe Nepomuceno
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


class MyGroupBox(widget.GroupBox):
    def draw(self):
        self.drawer.clear(self.background or self.bar.background)

        offset = self.margin_x
        for i, g in enumerate(self.groups):
            to_highlight = False
            is_block = self.highlight_method == "block"
            is_line = self.highlight_method == "line"

            bw = self.box_width([g])

            if self.group_has_urgent(g) and self.urgent_alert_method == "text":
                text_color = self.urgent_text
            elif g.windows:
                text_color = self.active
            else:
                text_color = self.inactive

            if g.screen:
                if self.highlight_method == "text":
                    border = None
                    if self.bar.screen.group.name == g.name:
                        if self.qtile.current_screen == self.bar.screen:
                            text_color = self.this_current_screen_border
                            to_highlight = True
                        else:
                            text_color = self.this_screen_border
                    else:
                        if self.qtile.current_screen == g.screen:
                            text_color = self.other_current_screen_border
                        else:
                            text_color = self.other_screen_border
                else:
                    if self.block_highlight_text_color:
                        text_color = self.block_highlight_text_color
                    if self.bar.screen.group.name == g.name:
                        if self.qtile.current_screen == self.bar.screen:
                            border = self.this_current_screen_border
                            to_highlight = True
                        else:
                            border = self.this_screen_border
                    else:
                        if self.qtile.current_screen == g.screen:
                            border = self.other_current_screen_border
                        else:
                            border = self.other_screen_border
            elif self.group_has_urgent(g) and self.urgent_alert_method in (
                "border",
                "block",
                "line",
            ):
                border = self.urgent_border
                if self.urgent_alert_method == "block":
                    is_block = True
                elif self.urgent_alert_method == "line":
                    is_line = True
            else:
                border = None

            self.drawbox(
                offset,
                g.label,
                border,
                text_color,
                highlight_color=self.highlight_color,
                width=bw,
                rounded=self.rounded,
                block=is_block,
                line=is_line,
                highlighted=to_highlight,
            )
            offset += bw + self.spacing
        self.drawer.draw(offsetx=self.offset, offsety=self.offsety, width=self.width)
