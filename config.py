"""
Copyright (c) 2010 Aldo Cortesi
Copyright (c) 2010, 2014 dequis
Copyright (c) 2012 Randall Ma
Copyright (c) 2012-2014 Tycho Andersen
Copyright (c) 2012 Craig Barnes
Copyright (c) 2013 horsik
Copyright (c) 2013 Tao Sauvage
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import subprocess

from libqtile import hook

from settings.color_theme import init_theme
from settings.groups import init_groups
from settings.keys import init_keybindings
from settings.layouts import init_floating_layout, init_floating_types, init_layouts
from settings.mouse import init_mouse_settings
from settings.screens import init_screens

wmname = "LG3D"

follow_mouse_focus = False
cursor_warp = False
bring_front_click = False

auto_fullscreen = True
auto_minimize = False

focus_on_window_activation = "focus"  # Options: "focus", "smart"

main = None

# Colors
colors = init_theme()

# Groups
groups = init_groups()

# Keybindings
keys = init_keybindings(groups=groups)

# Layouts
layouts = init_layouts(colors=colors)
floating_types = init_floating_types()
floating_layout = init_floating_layout(colors=colors)

# Screens
screens = init_screens()

# Mouse
mouse = init_mouse_settings()


# Client default group assignment helper
def _send_client_to_group(client, group):
    client.togroup(group)
    client.group.cmd_toscreen(toggle=False)


def _assign_client_to_default_group(client, **kwargs):
    wm_class_default_group = kwargs["wm_class_default_group"]
    wm_name_default_group = kwargs["wm_name_default_group"]
    excluded_wm_roles = kwargs["excluded_wm_roles"]

    # Find out if client has a default group specified or it is to be excluded.
    group = None  # Assume client has no default group

    wm_class = client.get_wm_class()[0].lower()
    if wm_class in wm_class_default_group:
        group = wm_class_default_group[wm_class]
        # HACK: Telegram and Steam get caught in below check for wm_role, so send them
        # to the correct group immediately.
        if wm_class in {"telegram-desktop", "steamwebhelper"}:
            _send_client_to_group(client, group)

    wm_name = client.name.lower()
    if wm_name in wm_name_default_group:
        group = wm_name_default_group[wm_name]

    wm_role = client.get_wm_role() is not None and client.get_wm_role().lower()
    # wm_role = client.get_wm_role().lower()
    if wm_role in excluded_wm_roles:
        return

    # Move client to default group.
    if group:
        _send_client_to_group(client, group)


# Hooks
@hook.subscribe.client_new
def assign_app_group(client):
    HOME = "home"
    WEB = "web"
    MISC = "misc"
    LAB = "lab"
    FILE = "file"
    RELAX = "relax"
    NOTES = "notes"
    CONF = "conf"
    MUSIC = "music"
    MAIL = "mail"

    # Specify the default group of wm_classes and wm_names.
    # NOTE: Keys MUST be in all lower case.
    wm_class_default_group = {
        "discord": MAIL,
        "gimp": RELAX,
        "gimp-2.10": RELAX,
        "gl": RELAX,
        "insomnia": LAB,
        "libreoffice-calc": MAIL,
        "mail": MAIL,
        "mpv": RELAX,
        "steam": RELAX,
        "steamwebhelper": RELAX,
        "telegram-desktop": MAIL,
        "telegramdesktop": MAIL,
        "thunar": FILE,
        "thunderbird": MAIL,
        "vlc": RELAX,
    }
    wm_name_default_group = {
        "neorg": NOTES,
        "steam": RELAX,
        "telegram (1)": MAIL,
    }

    # Specify the wm_roles to exclude from above a specification.
    # Differentiate between windows of same class or with same title but with different
    # roles, i.e. with different desired behaviour, like floating.
    # NOTE: Values MUST be in all lower case.
    excluded_wm_roles = {
        "float",
        "floatnote",
        "floatterm",
        "floatwin",
    }

    group_assignment_rules = {
        "wm_class_default_group": wm_class_default_group,
        "wm_name_default_group": wm_name_default_group,
        "excluded_wm_roles": excluded_wm_roles,
    }
    _assign_client_to_default_group(client, **group_assignment_rules)


# Hooks
@hook.subscribe.startup_once
def start_once():
    HOME = os.path.expanduser("~")
    subprocess.call([f"{HOME}/.config/qtile/scripts/autostart.sh"])


@hook.subscribe.client_new
def set_floating(window):
    if (
        window.window.get_wm_transient_for()
        or window.window.get_wm_type() in floating_types
    ):
        window.floating = True
