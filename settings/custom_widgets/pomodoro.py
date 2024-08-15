import subprocess
from datetime import datetime, timedelta

from libqtile.command.base import expose_command
from libqtile.widget.base import ThreadPoolText


class MyPomodoro(ThreadPoolText):
    defaults = [
        ("minutes_focus", 25, "Focus session length in minutes"),
        ("text_initial", "POMODORO", "Text as a reminder to start using the timer"),
        ("text_paused", "Paused  ", "Text when timer is paused"),
        ("text_timeup", "Time Up ", "Text when time is up"),
        ("prefix_inactive", "", "Prefix before any use, is paused or time is up"),
        ("prefix_focus", "", "Prefix when in focus state"),
        ("prefix_short_break", "", "Prefix when in short break state"),
        ("prefix_long_break", "", "Prefix when in long break state"),
        ("color_inactive", "#FF0000", "Color of `text_initial`"),
        ("color_focus", "#00FF00", "Color of text when in focus state"),
        ("color_short_break", "#0000FF", "Color of text when in short break state"),
        ("color_long_break", "#0000FF", "Color of text when in long break state"),
        ("notification", True, "Enable notifications when time is up"),
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

        self.color = {
            "inactive": self.color_inactive,
            MyPomodoro.STATE_FOCUS: self.color_focus,
            MyPomodoro.STATE_SHORT_BREAK: self.color_short_break,
            MyPomodoro.STATE_LONG_BREAK: self.color_long_break,
        }
        self.prefix = {
            "inactive": self.prefix_inactive,
            MyPomodoro.STATE_FOCUS: self.prefix_focus,
            MyPomodoro.STATE_SHORT_BREAK: self.prefix_short_break,
            MyPomodoro.STATE_LONG_BREAK: self.prefix_long_break,
        }

    def poll(self):
        if not self.is_active:
            self.foreground = self.color["inactive"]
            prefix = self.prefix["inactive"]
            text = self.text_initial
            return self._format_text(prefix, text)

        time_now = datetime.now()
        if self.is_paused:
            self.foreground = self.color["inactive"]
            prefix = self.prefix["inactive"]
            text = self.text_paused
        elif self.state_time_end > time_now:
            self.state_time_left = self.state_time_end - time_now
            self.foreground = self.color[self.state]
            prefix = self.prefix[self.state]
            text = self._format_time(self.state_time_left)
        else:
            self._send_notification(self.text_timeup)
            self.is_timeup = True
            self.foreground = self.color["inactive"]
            prefix = self.prefix["inactive"]
            text = self.text_timeup
        return self._format_text(prefix, text)

    def _format_time(self, time: timedelta) -> str:
        return "%02d:%02d:%02d" % (
            time.seconds // 3600,
            time.seconds % 3600 // 60,
            time.seconds % 60,
        )

    def _format_text(self, prefix, text):
        return f"{prefix}{text}"

    @expose_command
    def start(self):
        if not self.is_active or self.is_timeup:
            self._determine_upcoming_state()
            self.is_active = True
            self.is_timeup = False
            self._close_notification()
            self.notify_timup = True  # Re-enable notification
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
            self._send_notification(self.text_paused)
            self.notify_timup = True  # Notify when countdown is up or paused again
        else:
            self.is_paused = False
            self.state_time_end = datetime.now() + timedelta(
                seconds=self.state_time_left.seconds
            )
            self._close_notification()

    def _send_notification(self, message):
        """Requires `dunst` installed on system"""
        if not self.notification:
            return
        if self.notify_timup:
            title = "Pomodoro"
            text = f"{self.state.replace('_', ' ').title()}: {message}"
            urgency = "critical"
            subprocess.run(
                ["dunstify", title, text, f"--urgency={urgency}"], shell=False
            )
        self.notify_timup = False  # Prevent spamming notifications from `.poll()`

    def _close_notification(self):
        """Requires `dunst` installed on system"""
        if not self.notification:
            return
        subprocess.run(["dunstctl", "close"], shell=False)
