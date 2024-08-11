from datetime import datetime, timedelta

from libqtile.widget.base import ThreadPoolText


class MyPomodoro(ThreadPoolText):
    defaults = []
    UPDATE_INTERVAL_SECONDS = 1

    def __init__(self, **config):
        config["update_interval"] = MyPomodoro.UPDATE_INTERVAL_SECONDS  # Force apply
        super().__init__("", **config)
        self.add_defaults(MyPomodoro.defaults)

        self.state_time_end = datetime.now() + timedelta(minutes=25)

    def poll(self):
        time_now = datetime.now()
        state_time_remaining = self.state_time_end - time_now

        if self.state_time_end > time_now:
            text = self._format_time(state_time_remaining)
        else:
            text = "Time Up "
        return text

    def _format_time(self, time: timedelta) -> str:
        return "%02d:%02d:%02d" % (
            time.seconds // 3600,
            time.seconds % 3600 // 60,
            time.seconds % 60,
        )
