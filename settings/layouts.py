from libqtile import layout
from libqtile.config import Match


def layout_defaults(colors: dict, **kwargs: dict):
    return {
        "margin": kwargs.get("margin", 5),
        "border_width": kwargs.get("border_width", 3),
        "border_focus": kwargs.get("border_focus", colors["primary"][1]),
        "border_normal": kwargs.get("border_normal", colors["bg"]),
    }


def init_layouts(colors: dict):
    return [
        layout.MonadTall(**layout_defaults(colors)),
        layout.MonadWide(ratio=0.75, **layout_defaults(colors)),
        # layout.Matrix(**layout_defaults(colors)),
        # layout.Bsp(**layout_defaults(colors)),
        # layout.Floating(**layout_defaults(colors)),
        # layout.RatioTile(**layout_defaults(colors)),
        # layout.Max(**layout_defaults(colors)),
    ]


def init_floating_types():
    return ["notification", "toolbar", "splash", "dialog"]


def init_floating_layout(colors: dict):
    float_rules = [
        # Run the utility of `xprop` to see the wm class and title of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(title="branchdialog"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="Arandr"),
        Match(wm_class="feh"),
        Match(wm_class="Galculator"),
        Match(wm_class="archlinux-logout"),
        Match(wm_class="matplotlib"),
        Match(title="Create Snapshot", wm_class="Timeshift-gtk"),
        # Scripts
        # NOTE: The `Match` object will return true (a match) on substrings!
        # `Match(title="Neorg")` will match with ANY window with "Neorg" in its title,
        # for example: "NeorgNote", "NoteNeorg", etc.
        # Therefor the combined attributes need to be unique for a unique match.
        Match(title="Neorg", role="FloatNote"),
    ]

    return layout.Floating(
        float_rules=float_rules,
        fullscreen_border_width=0,
        **layout_defaults(
            colors,
            **{
                "border_normal": colors["dim"][0],
            }
        )
    )
