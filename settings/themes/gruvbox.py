def init_theme():
    """An altered and extended Gruvbox color pallet."""
    # Theme colors
    black = ["#282828", "#928374"]
    red = ["#CC241D", "#FB4934"]
    green = ["#689D6A", "#8EC07C"]
    yellow = ["#D79921", "#FABD2F"]
    blue = ["#458588", "#83A598"]
    purple = ["#B16286", "#D3869B"]
    cyan = ["#98971A", "#B8BB26"]
    white = ["#A89984", "#EBDBB2"]
    # Extended colors
    dim = ["#504945", "#807670"]
    orange = ["#D65D0E", "#FE8019"]
    return {
        # Main colors
        "black": black,
        "red": red,
        "green": green,
        "yellow": yellow,
        "blue": blue,
        "purple": purple,
        "cyan": cyan,
        "white": white,
        "orange": orange,
        # Special colors
        "bg": black[0],
        "fg": white[1],
        "primary": orange,
        "secondary": yellow,
        "accent": blue,
        "dim": dim,
        "warning": yellow[1],
        "danger": orange[1],
        "critical": red[1],
        "volume_min": green[1],
        "volume_med": yellow[1],
        "volume_max": orange[1],
    }
