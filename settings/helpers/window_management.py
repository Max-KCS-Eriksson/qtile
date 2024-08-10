from libqtile.lazy import lazy


def _window_to_group(qtile, direction=None):
    if qtile.currentWindow or direction is None:
        return

    i = qtile.groups.index(qtile.currentGroup)
    destination = i + direction
    qtile.currentWindow.togroup(qtile.groups[destination].name)


@lazy.function
def window_to_prev_group(qtile):
    direction = -1
    _window_to_group(qtile, direction)


@lazy.function
def window_to_next_group(qtile):
    direction = 1
    _window_to_group(qtile, direction)


def _window_to_screen(qtile, destination=None, switch_group=False, switch_screen=False):
    if destination is None:
        return

    group = qtile.screens[destination].group.name
    qtile.current_window.togroup(group, switch_group=switch_group)
    if switch_screen:
        qtile.cmd_to_screen(destination)


def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    destination = i - 1
    if i == 0:
        destination = len(qtile.screens) - 1
    _window_to_screen(qtile, destination, switch_group, switch_screen)


def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    destination = i + 1
    if i == len(qtile.screens) - 1:
        destination = 0
    _window_to_screen(qtile, destination, switch_group, switch_screen)
