import psutil
from libqtile.widget import base

# TODO: Widget class not implemented!


class MyCpuIcon(base.ThreadPoolText):
    def __init__(self) -> None:
        raise NotImplementedError
        super().__init__()

    def poll(self):
        raise NotImplementedError
        cpu_percent = psutil.cpu_percent()
        return super().poll()
