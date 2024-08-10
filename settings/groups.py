from libqtile.config import Group


def init_groups():
    return [
        Group(
            # name="1",
            name="home",
            layout="monadwide",
            label="",  #         
            layout_opts=None,  # Options to pass to a layout.
            screen_affinity=None,  # Preference to start on specific screen.
            spawn=None,
        ),
        Group(
            # name="2",
            name="web",
            layout="monadtall",
            label=" ",  #   
            layout_opts=None,  # Options to pass to a layout.
            screen_affinity=None,  # Preference to start on specific screen.
            spawn=None,
        ),
        Group(
            # name="3",
            name="misc",
            layout="monadtall",
            label="",  #   
            layout_opts=None,  # Options to pass to a layout.
            screen_affinity=None,  # Preference to start on specific screen.
            spawn=None,
        ),
        Group(
            # name="4",
            name="lab",
            layout="monadwide",
            label="",  #   
            layout_opts=None,  # Options to pass to a layout.
            screen_affinity=None,  # Preference to start on specific screen.
            spawn=None,
        ),
        Group(
            # name="5",
            name="file",
            layout="monadtall",
            label="",  #   
            layout_opts=None,  # Options to pass to a layout.
            screen_affinity=None,  # Preference to start on specific screen.
            spawn=None,
        ),
        Group(
            # name="6",
            name="relax",
            layout="monadtall",
            label="",  # 
            layout_opts=None,  # Options to pass to a layout.
            screen_affinity=None,  # Preference to start on specific screen.
            spawn=None,
        ),
        Group(
            # name="7",
            name="notes",
            layout="monadtall",
            label="",  #       
            layout_opts=None,  # Options to pass to a layout.
            screen_affinity=None,  # Preference to start on specific screen.
            spawn=None,
        ),
        Group(
            # name="8",
            name="conf",
            layout="monadtall",
            label="",  #     
            layout_opts=None,  # Options to pass to a layout.
            screen_affinity=None,  # Preference to start on specific screen.
            spawn=None,
        ),
        Group(
            # name="9",
            name="music",
            layout="monadtall",
            label="",  # 
            layout_opts=None,  # Options to pass to a layout.
            screen_affinity=None,  # Preference to start on specific screen.
            spawn=None,
        ),
        Group(
            # name="0",
            name="mail",
            layout="monadtall",
            label="",  #     @    
            layout_opts=None,  # Options to pass to a layout.
            screen_affinity=None,  # Preference to start on specific screen.
            spawn=None,
        ),
    ]
