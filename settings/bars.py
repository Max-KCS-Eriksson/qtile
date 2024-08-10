from libqtile import bar
from libqtile.widget.spacer import Spacer

from . import color_theme, widgets

# Color theme and fonts
COLORS = color_theme.init_theme()
BACKGROUND = COLORS["bg"]

# Default bar kwargs
bar_defaults = dict(
    size=26,
    background=BACKGROUND,
    opacity=1,
)


def init_main_bar():
    widgets_list = [
        # Left
        widgets.get_custom_workspaces(),
        widgets.sep,
        widgets.get_current_screen_indicator(),
        widgets.sep,
        widgets.get_current_layout_icon(),
        widgets.get_current_layout(),
        widgets.sep,
        widgets.webpage_monitor_icon,
        widgets.webpage_monitor_widget,
        # Center
        widgets.spacer,
        widgets.get_weekday(),
        widgets.sep,
        widgets.get_week_number(),
        widgets.sep,
        widgets.get_time(),
        widgets.sep,
        widgets.get_date(),
        widgets.spacer,
        # Right
        widgets.memory_icon,
        widgets.memory,
        widgets.sep,
        widgets.cpu_icon,
        widgets.cpu,
        widgets.sep,
        widgets.disk_icon,
        widgets.disk,
        widgets.sep,
        widgets.backlight_icon,
        # widgets.custom_backlight_icon,
        # widgets.backlight,
        widgets.custom_backlight,
        widgets.sep,
        widgets.volume_icon,
        # widgets.custom_volume_icon,
        # widgets.volume,
        widgets.custom_volume,
        widgets.sep,
        widgets.sys_tray,
        Spacer(length=2),
        widgets.sep,
        widgets.battery_icon,
        widgets.battery,
        widgets.sep,
        widgets.poweroff,
        Spacer(length=5),
    ]

    return bar.Bar(widgets=widgets_list, **bar_defaults)


def init_secondary_bar():
    widgets_list = [
        # Left
        widgets.get_custom_workspaces(),
        widgets.sep,
        widgets.get_current_screen_indicator(),
        widgets.sep,
        widgets.get_current_layout_icon(),
        widgets.get_current_layout(),
        widgets.sep,
        widgets.webpage_monitor_icon,
        widgets.webpage_monitor_widget,
        # Center
        widgets.spacer,
        widgets.get_weekday(),
        widgets.sep,
        widgets.get_week_number(),
        widgets.sep,
        widgets.get_time(),
        widgets.sep,
        widgets.get_date(),
        widgets.spacer,
        # Right
        widgets.memory_icon,
        widgets.memory,
        widgets.sep,
        widgets.cpu_icon,
        widgets.cpu,
        widgets.sep,
        widgets.disk_icon,
        widgets.disk,
        widgets.sep,
        widgets.backlight_icon,
        # widgets.custom_backlight_icon,
        # widgets.backlight,
        widgets.custom_backlight,
        widgets.sep,
        widgets.volume_icon,
        # widgets.custom_volume_icon,
        # widgets.volume,
        widgets.custom_volume,
        widgets.sep,
        widgets.battery_icon,
        widgets.battery,
        widgets.sep,
        widgets.poweroff,
        Spacer(length=5),
    ]

    return bar.Bar(widgets=widgets_list, **bar_defaults)
