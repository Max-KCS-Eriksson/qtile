from datetime import datetime, timedelta

from libqtile.command.base import expose_command
from libqtile.widget.base import ThreadPoolText


class MyPomodoro(ThreadPoolText):
    defaults = [
        ("minutes_focus", 25, "Focus session length in minutes"),
    ]
    UPDATE_INTERVAL_SECONDS = 1

    NUM_POMODOROS = 4
    STATE_FOCUS = "focus"
    STATE_SHORT_BREAK = "short_break"
    STATE_LONG_BREAK = "long_break"

    def __init__(self, **config):
        config["update_interval"] = MyPomodoro.UPDATE_INTERVAL_SECONDS  # Force apply
        super().__init__("", **config)
        self.add_defaults(MyPomodoro.defaults)

        self.is_active = False
        self.is_paused = False
        self.is_timeup = False

        self.completed_pomodoros = 0
        self.state = MyPomodoro.STATE_FOCUS

    def poll(self):
        if not self.is_active:
            return "POMODORO"

        time_now = datetime.now()
        if self.is_paused:
            text = "Paused  "
        elif self.state_time_end > time_now:
            self.state_time_left = self.state_time_end - time_now
            text = self._format_time(self.state_time_left)
        else:
            self.is_timeup = True
            text = "Time Up "
        return text

    def _format_time(self, time: timedelta) -> str:
        return "%02d:%02d:%02d" % (
            time.seconds // 3600,
            time.seconds % 3600 // 60,
            time.seconds % 60,
        )

    @expose_command
    def start(self):
        if not self.is_active or self.is_timeup:
            self._determine_upcoming_state()
            self.is_active = True
            self.is_timeup = False
        else:
            self._toggle_pause()

    def _determine_upcoming_state(self):
        if not self.is_active or self.state != MyPomodoro.STATE_FOCUS:
            self.state = MyPomodoro.STATE_FOCUS
            self.state_time_end = datetime.now() + timedelta(minutes=self.minutes_focus)
        else:
            self.completed_pomodoros += 1
            if self.completed_pomodoros % MyPomodoro.NUM_POMODOROS != 0:
                self.state = MyPomodoro.STATE_SHORT_BREAK
                self.state_time_end = datetime.now() + timedelta(
                    minutes=self.minutes_focus / 5  # Pomodoro technique pattern
                )
            else:
                self.state = MyPomodoro.STATE_LONG_BREAK
                self.state_time_end = datetime.now() + timedelta(
                    minutes=self.minutes_focus / 5 * 3  # Pomodoro technique pattern
                )
        self.state_time_left = self.state_time_end

    def _toggle_pause(self):
        if not self.is_paused:
            self.is_paused = True
        else:
            self.is_paused = False
            self.state_time_end = datetime.now() + timedelta(
                seconds=self.state_time_left.seconds
            )
