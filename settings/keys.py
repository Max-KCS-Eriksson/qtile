from libqtile.config import Key
from libqtile.lazy import lazy

from .helpers.window_management import (
    window_to_next_screen,
    window_to_previous_screen,
)

# Modifiers
META = "mod4"
SHIFT = "shift"
CTRL = "control"
ALT = "mod1"

# Keys
UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"
HOME = "home"
END = "end"
TAB = "Tab"
SPACE = "space"
ESC = "Escape"


def init_keybindings(groups):
    """Qtile specific keybindings"""
    # Keybinds grouped in lists, and ordered by used modifiers
    # Example:
    # purpose_of_keys = [
    #   # Meta + key
    #   # Meta + Shift + key
    #   # Meta + Ctrl + key
    #   # Meta + Alt + key
    # ]

    qtile_keys = [
        # Meta + key
        # Meta + Shift + key
        Key([META, SHIFT], "r", lazy.restart()),
        # Meta + Ctrl + key
        Key([META, CTRL], "r", lazy.reload_config()),
        # Meta + Alt + key
    ]

    window_keys = [
        # Meta + key
        Key([META], ESC, lazy.window.kill()),
        # Meta + Shift + key
        Key([META, SHIFT], "q", lazy.window.kill()),
        Key([META, SHIFT], "f", lazy.window.toggle_fullscreen()),
        Key(  # Move window between screens
            [META, SHIFT],
            END,
            lazy.function(window_to_next_screen, switch_screen=True),
        ),
        Key(  # Move window between screens
            [META, SHIFT],
            HOME,
            lazy.function(window_to_previous_screen, switch_screen=True),
        ),
        # Meta + Ctrl + key
        # Meta + Alt + key
        Key([META, ALT], "f", lazy.window.toggle_floating()),
    ]

    layout_keys = [
        # Meta + key
        Key([META], UP, lazy.layout.up()),  # Change focus
        Key([META], DOWN, lazy.layout.down()),  # Change focus
        Key([META], LEFT, lazy.layout.left()),  # Change focus
        Key([META], RIGHT, lazy.layout.right()),  # Change focus
        Key([META], "k", lazy.layout.up()),  # Change focus
        Key([META], "j", lazy.layout.down()),  # Change focus
        Key([META], "h", lazy.layout.left()),  # Change focus
        Key([META], "l", lazy.layout.right()),  # Change focus
        Key([META], TAB, lazy.group.next_window()),  # Cycle windows
        # Meta + Shift + key
        Key([META, SHIFT], TAB, lazy.group.prev_window()),  # Cycle windows back
        Key([META, SHIFT], SPACE, lazy.next_layout()),  # Cycle layouts
        Key([META, SHIFT], "n", lazy.layout.normalize()),
        Key([META, SHIFT], "t", lazy.layout.flip()),  # Mirror layout
        Key([META, SHIFT], "k", lazy.layout.shuffle_up()),  # Move windows in BSP
        Key([META, SHIFT], "j", lazy.layout.shuffle_down()),  # Move windows in BSP
        Key([META, SHIFT], "h", lazy.layout.shuffle_left()),  # Move windows in BSP
        Key([META, SHIFT], "l", lazy.layout.shuffle_right()),  # Move windows in BSP
        Key([META, SHIFT], UP, lazy.layout.shuffle_up()),  # Move windows in Monad*
        Key([META, SHIFT], DOWN, lazy.layout.shuffle_down()),  # Move windows in Monad*
        Key([META, SHIFT], LEFT, lazy.layout.swap_left()),  # Move windows in Monad*
        Key([META, SHIFT], RIGHT, lazy.layout.swap_right()),  # Move windows in Monad*
        # Meta + Ctrl + key
        Key(  # Resize window
            [META, CTRL],
            "l",
            lazy.layout.grow_right(),
            lazy.layout.grow(),
            lazy.layout.increase_ratio(),
            lazy.layout.delete(),
        ),
        Key(  # Resize window
            [META, CTRL],
            RIGHT,
            lazy.layout.grow_right(),
            lazy.layout.grow(),
            lazy.layout.increase_ratio(),
            lazy.layout.delete(),
        ),
        Key(  # Resize window
            [META, CTRL],
            "h",
            lazy.layout.grow_left(),
            lazy.layout.shrink(),
            lazy.layout.decrease_ratio(),
            lazy.layout.add(),
        ),
        Key(  # Resize window
            [META, CTRL],
            LEFT,
            lazy.layout.grow_left(),
            lazy.layout.shrink(),
            lazy.layout.decrease_ratio(),
            lazy.layout.add(),
        ),
        Key(  # Resize window
            [META, CTRL],
            "k",
            lazy.layout.grow_up(),
            lazy.layout.grow(),
            lazy.layout.decrease_nmaster(),
        ),
        Key(  # Resize window
            [META, CTRL],
            UP,
            lazy.layout.grow_up(),
            lazy.layout.grow(),
            lazy.layout.decrease_nmaster(),
        ),
        Key(  # Resize window
            [META, CTRL],
            "j",
            lazy.layout.grow_down(),
            lazy.layout.shrink(),
            lazy.layout.increase_nmaster(),
        ),
        Key(  # Resize window
            [META, CTRL],
            DOWN,
            lazy.layout.grow_down(),
            lazy.layout.shrink(),
            lazy.layout.increase_nmaster(),
        ),
        # Meta + Alt + key
        Key([META, ALT], "k", lazy.layout.flip_up()),  # Flip layout for BSP
        Key([META, ALT], "j", lazy.layout.flip_down()),  # Flip layout for BSP
        Key([META, ALT], "l", lazy.layout.flip_right()),  # Flip layout for BSP
        Key([META, ALT], "h", lazy.layout.flip_left()),  # Flip layout for BSP
    ]

    group_keys = [
        # Meta + key
        # Meta + Shift + key
        # Meta + Ctrl + key
        # Meta + Alt + key
    ]

    screen_focus_keys = [
        # Meta + key
        Key([META], HOME, lazy.prev_screen(), desc="Focus prev monitor"),
        Key([META], END, lazy.next_screen(), desc="Focus next monitor"),
        # Meta + Shift + key
        # Meta + Ctrl + key
        Key(
            [META, CTRL],
            "1",
            lazy.to_screen(2),  # NOTE: Setup specific
            desc="Focus monitor 1",
        ),
        Key(
            [META, CTRL],
            "2",
            lazy.to_screen(0),  # NOTE: Setup specific
            desc="Focus monitor 2",
        ),
        Key(
            [META, CTRL],
            "3",
            lazy.to_screen(1),  # NOTE: Setup specific
            desc="Focus monitor 3",
        ),
        # Meta + Alt + key
    ]

    # Group specific keybinds
    FIRST_NUMROW_KEY = 1
    LAST_NUMROW_KEY = 0
    for i, group in enumerate(groups, start=FIRST_NUMROW_KEY):
        if i == 10:
            i = LAST_NUMROW_KEY
        numkey = str(i)

        _group_keys = [
            # Change workspaces
            Key([META], numkey, lazy.group[group.name].toscreen()),
            # Move window to selected workspace 1-10 and stay on workspace
            Key([META, ALT], numkey, lazy.window.togroup(group.name)),
            # Move window to selected workspace 1-10 and follow to workspace
            Key(
                [META, SHIFT],
                numkey,
                lazy.window.togroup(group.name),
                lazy.group[group.name].toscreen(),
            ),
        ]

        group_keys.extend(_group_keys)

    return qtile_keys + window_keys + layout_keys + group_keys + screen_focus_keys
