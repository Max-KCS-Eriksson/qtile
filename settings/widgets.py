import subprocess
from pathlib import Path

from libqtile import bar, widget

from . import color_theme, custom_widgets
from .custom_widgets.backlight import MyBacklight
from .custom_widgets.backlight_icon import MyBacklightIcon
from .custom_widgets.cpu_icon import MyCpuIcon
from .custom_widgets.df_icon import MyDfIcon
from .custom_widgets.groupbox import MyGroupBox
from .custom_widgets.memory_icon import MyMemoryIcon
from .custom_widgets.pomodoro import MyPomodoro
from .custom_widgets.volume import MyVolume
from .custom_widgets.volume_icon import MyVolumeIcon
from .webpage_monitor import webpage_monitor

BASE_DIR = Path(__file__).resolve().parent.parent

# Apps
TERMINAL = "xfce4-terminal"

# Color theme and fonts
COLORS = color_theme.init_theme()
BACKGROUND = COLORS["bg"]
FOREGROUND = COLORS["fg"]
DIM_DARK = COLORS["dim"][0]
DIM_LIGHT = COLORS["dim"][1]

VOLUME_MIN_COLOR = COLORS["volume_min"]
VOLUME_MED_COLOR = COLORS["volume_med"]
VOLUME_MAX_COLOR = COLORS["volume_max"]

ICON_FONT = "Font Awesome 6 Free Solid, Solid"
ICON_SIZE = 14
ICON_COLOR = COLORS["dim"][0]

FONT = "JetBrainsMono Nerd Font"
FONT_BOLD = "JetBrainsMono Nerd Font bold"
FONT_SIZE = 14


# Default widget kwargs
icon_defaults = dict(
    font=ICON_FONT,
    fontsize=ICON_SIZE,
    background=BACKGROUND,
    foreground=ICON_COLOR,
)

text_defaults = dict(
    font=FONT,
    fontsize=FONT_SIZE,
    background=BACKGROUND,
    foreground=FOREGROUND,
)

# Separators and Spacers
sep = widget.Sep(
    size_percent=60,
    linewidth=1,
    padding=10,
    foreground=DIM_DARK,
    background=BACKGROUND,
)

spacer = widget.Spacer(length=bar.STRETCH)


# Widgets
def get_workspaces():
    return widget.GroupBox(
        font=ICON_FONT,
        fontsize=ICON_SIZE,
        center_aligned=True,
        margin_y=4,
        margin_x=5,
        padding_y=0,
        padding_x=0,
        borderwidth=2,
        disable_drag=True,
        active=COLORS["secondary"][1],
        inactive=DIM_DARK,
        rounded=False,
        highlight_method="line",  # options: border, text, block, line
        highlight_color=COLORS["primary"][
            1
        ],  # Active group highlight color when using 'line' highlight method.
        block_highlight_text_color=COLORS["primary"][1],  # Selected group font color
        this_current_screen_border=COLORS["primary"][
            1
        ],  # Focused screens current workspace
        this_screen_border=COLORS["secondary"][
            1
        ],  # Unfocused screens current workspace
        # other_current_screen_border=FOREGROUND,
        other_screen_border=DIM_DARK,  # ["fg"],
        urgent_alert_method="line",  # options: border, text, block, line
        urgent_border=COLORS["critical"],
        urgent_text=COLORS["critical"],
        # foreground=FOREGROUND,  # No role - use active/inactive
        background=BACKGROUND,
    )


def get_current_screen_indicator():
    return widget.CurrentScreen(
        font=ICON_FONT,
        fontsize=ICON_SIZE * 0.85,
        active_text="",  #   
        active_color=COLORS["primary"][1],
        inactive_text="",
        inactive_color=DIM_DARK,
        background=BACKGROUND,
    )


def get_current_layout_icon():
    return widget.CurrentLayoutIcon(
        scale=0.5,
        use_mask=True,
        padding=5,
        background=BACKGROUND,
    )


def get_current_layout():
    return widget.CurrentLayout(**text_defaults)


caps_num_lock_indicator = widget.CapsNumLockIndicator(**icon_defaults)

POMODORO = custom_widgets.pomodoro.MyPomodoro(
    # minutes_focus=0.2,  # FIX: For demo only. Use default
    notification=True,
    prefix_inactive="  ",  #     
    prefix_focus="  ",  #   
    prefix_short_break="  ",  # 
    prefix_long_break="  ",  # 
    color_inactive=COLORS["red"][1],
    color_focus=COLORS["purple"][1],
    color_short_break=COLORS["green"][1],
    color_long_break=COLORS["green"][1],
    markup=True,
    fmt_inactive="<b>{}</b>",
    fmt_focus="{}",
    fmt_short_break="<b>{}</b>",
    fmt_long_break="<b>{}</b>",
    padding=5,
    **text_defaults,
)

webpage_monitor_icon = widget.TextBox(  # Poll / Script Icon
    text="",  # Font Awesome -  
    padding=5,
    **icon_defaults,
)

webpage_monitor_widget = widget.GenPollText(  # Webpage monitor
    update_interval=3600,  # 3600 seconds = 1 hour
    func=lambda: webpage_monitor.check_once(),  # Function need to return a string.
    markup=True,  # Allow styling from markup in returned string.
    **text_defaults,
)


def get_weekday():
    return widget.Clock(  # Weekday
        format="%a",
        font=FONT,
        fontsize=FONT_SIZE,
        background=BACKGROUND,
        foreground=DIM_DARK,
    )


def get_week_number():
    return widget.Clock(  # Week number
        format="w%V",
        font=FONT,
        fontsize=FONT_SIZE,
        background=BACKGROUND,
        foreground=DIM_DARK,
    )


def get_time():
    return widget.Clock(  # Time
        format="%H:%M:%S",
        fontsize=FONT_SIZE,
        font=FONT,
        background=BACKGROUND,
        foreground=FOREGROUND,
    )


def get_date():
    return widget.Clock(  # Date
        format="%y-%m-%d",
        font=FONT,
        fontsize=FONT_SIZE,
        background=BACKGROUND,
        foreground=DIM_DARK,
    )


memory_icon = widget.TextBox(  # Memory Icon
    text="",  # Nerd Font
    padding=10,
    font="JetBrainsMono Nerd Font",
    fontsize=ICON_SIZE,
    background=BACKGROUND,
    foreground=ICON_COLOR,
)

memory = widget.Memory(
    update_interval=1,
    measure_mem="G",  # Options: "G", "M"
    format="{MemPercent:.0f} %",
    **text_defaults,
)

cpu_icon = widget.TextBox(  # CPU Icon
    text="",  # Font Awesome
    padding=5,
    **icon_defaults,
)

cpu = widget.CPU(
    update_interval=1,
    format="{load_percent:.0f} %",
    **text_defaults,
)

disk_icon = widget.TextBox(  # Disk Icon
    text="",  # Font Awesome -     
    padding=5,
    font=ICON_FONT,
    fontsize=ICON_SIZE - 2,
    background=BACKGROUND,
    foreground=ICON_COLOR,
)

disk = widget.DF(
    update_interval=60,
    measure="G",
    partition="/",
    visible_on_warn=False,
    format="{r:.0f} %",
    **text_defaults,
)

backlight_icon = widget.TextBox(  # Backlight Icon
    text="",  # Font Awesome -   
    padding=5,
    **icon_defaults,
)

backlight = widget.Backlight(
    update_interval=0.2,
    backlight_name="amdgpu_bl0",
    brightness_file="/sys/class/backlight/amdgpu_bl0/brightness",
    max_brightness_file="/sys/class/backlight/amdgpu_bl0/max_brightness",
    format="{percent:.0%} %",
    **text_defaults,
)

volume_icon = widget.TextBox(  # Volume Icon
    text="",  # Font Awesome  
    padding=5,
    **icon_defaults,
)

sys_tray_icon = widget.TextBox(  # Sys Tray Icon
    text="",  # Font Awesome - 
    padding=5,
    **icon_defaults,
)

sys_tray = widget.Systray(
    icon_size=ICON_SIZE,
    background=BACKGROUND,
    padding=5,
)

poweroff = widget.TextBox(  # Poweroff widget
    text="",  # Font Awesome
    font=ICON_FONT,
    fontsize=ICON_SIZE + 2,
    background=BACKGROUND,
    foreground=COLORS["critical"],
    padding=5,
    mouse_callbacks={
        "Button1": lambda: subprocess.run(["loginctl", "poweroff"]),  # Left click
        "Button3": lambda: subprocess.run(["loginctl", "reboot"]),  # Right click
    },
)

countdown_poweroff = widget.QuickExit(
    default_text="",  # Font Awesome
    countdown_format="<span font='JetBrainsMono Nerd Font'>{}</span>",
    countdown_start=10,
    timer_interval=1,
    font=ICON_FONT,
    fontsize=ICON_SIZE + 2,
    background=BACKGROUND,
    foreground=COLORS["critical"],
    padding=5,
)

battery_icon = widget.TextBox(  # Battery Icon
    text="",  # Font Awesome -             
    padding=5,
    **icon_defaults,
)

battery = widget.Battery(
    update_interval=60,
    battery=0,
    charge_char="^",
    discharge_char="v",
    full_char="=",
    empty_char="x",
    unknown_char="?",
    format="{char} {percent:2.0%} {hour:d}:{min:02d}",  # TODO
    low_foreground=COLORS["critical"],
    low_percentage=0.25,
    **text_defaults,
)

nord_vpn_killswitch_status = widget.GenPollText(  # NordVPN Kill Switch status
    update_interval=1,
    func=lambda: 1,  # TODO: Make script to get info. Bash will work best.
    markup=True,
    **text_defaults,
)

vpn_status = widget.GenPollText(  # VPN status, TODO: Add CONST for VPN supplier
    update_interval=1,
    func=lambda: 1,  # TODO: Make script to get info. Bash will work best.
    markup=True,
    **text_defaults,
)


# Custom Widget classes.

custom_backlight_icon = custom_widgets.backlight_icon.MyBacklightIcon(
    update_interval=0.2,
    backlight_name="amdgpu_bl0",
    brightness_file="/sys/class/backlight/amdgpu_bl0/brightness",
    max_brightness_file="/sys/class/backlight/amdgpu_bl0/max_brightness",
    # change_command="<cmd> {0}",
    format="{percent}",
    icon=" ",  # Font Awesome -   
    low_color=ICON_COLOR,
    min_color=COLORS["yellow"][0],
    max_color=COLORS["yellow"][1],
    **text_defaults,
)

custom_backlight = custom_widgets.backlight.MyBacklight(
    update_interval=0.2,
    backlight_name="amdgpu_bl0",
    brightness_file="/sys/class/backlight/amdgpu_bl0/brightness",
    max_brightness_file="/sys/class/backlight/amdgpu_bl0/max_brightness",
    # change_command="<cmd> {0}",
    format="{percent}",
    **text_defaults,
)

custom_volume_icon = custom_widgets.volume_icon.MyVolumeIcon(
    icon="",  # Font Awesome  
    mute_color=ICON_COLOR,
    min_color=VOLUME_MIN_COLOR,
    med_color=VOLUME_MED_COLOR,
    max_color=VOLUME_MAX_COLOR,
    padding=5,
    **icon_defaults,
)

custom_volume = custom_widgets.volume.MyVolume(
    volume_app=None,
    volume_up_command=None,
    volume_down_command=None,
    step=5,
    padding=5,
    fmt="{}",
    **text_defaults,
)


def get_custom_workspaces():
    return custom_widgets.groupbox.MyGroupBox(
        center_aligned=True,
        margin_y=4,
        margin_x=5,
        padding_y=0,
        padding_x=0,
        borderwidth=2,
        disable_drag=True,
        rounded=False,
        highlight_method="text",  # options: border, text, block, line
        font=ICON_FONT,
        fontsize=ICON_SIZE,
        active=DIM_LIGHT,
        inactive=DIM_DARK,
        this_current_screen_border=COLORS["primary"][1],  # Focused screens workspace
        this_screen_border=COLORS["primary"][0],  # Unfocused screens workspace
        other_current_screen_border=COLORS["secondary"][1],  # Other screens workspace
        other_screen_border=COLORS["secondary"][0],  # Other unfocused screens workspace
        urgent_alert_method="line",  # options: border, text, block, line
        urgent_border=COLORS["critical"],
        urgent_text=COLORS["critical"],
        background=BACKGROUND,
    )
