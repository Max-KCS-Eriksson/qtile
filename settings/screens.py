from libqtile.config import Screen

from . import bars


def init_screens():
    return [
        Screen(
            top=bars.init_main_bar(),
        ),
        Screen(
            top=bars.init_secondary_bar(),
        ),
        Screen(
            top=bars.init_secondary_bar(),
        ),
    ]
