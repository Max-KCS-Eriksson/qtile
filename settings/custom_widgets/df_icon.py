import psutil
from libqtile.widget import base

# TODO: Widget class not implemented!


class MyDfIcon(base.ThreadPoolText):
    def __init__(self) -> None:
        raise NotImplementedError
        super().__init__()

    def poll(self):
        raise NotImplementedError
        df_percent = psutil.disk_usage("/").percent
        return super().poll()
