from datetime import timedelta

from libqtile.widget.clock import Clock


class MyClock(Clock):
    """Compensating that libqtile.widget.clock.Clock showing incorrect time."""

    DELTA = timedelta(minutes=17, seconds=0.5)
