import io
import traceback
from pathlib import Path
from logging.handlers import RotatingFileHandler
from utils.globals import ui_stream

from logging import (
    getLogger,
    Handler,
    Formatter,
    basicConfig,
    INFO,
    DEBUG,
    CRITICAL,
)

class UiHandler(Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        try:
            msg = self.format(record)
            ui_stream.push(msg)
            print("EEEE",ui_stream.text_list[-1])
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)

logs_path = Path("logs")
logs_path.mkdir(exist_ok=True, parents=True)

log = getLogger()
log.setLevel(INFO)

logging_format = "%(levelname)s [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s"
formatter = Formatter(logging_format)

ui_handler = UiHandler()
ui_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(filename=logs_path / "log.txt", mode="a", encoding="utf-8",backupCount=5,maxBytes=1024*1024*5) # 最大5MB
file_handler.setFormatter(formatter)

log.addHandler(ui_handler)
log.addHandler(file_handler)

flet = getLogger("flet")
flet.setLevel(CRITICAL)
flet_core = getLogger("flet_core")
flet_core.setLevel(CRITICAL)

basicConfig(level=INFO)

def set_debug(debug: bool = False):
    log.setLevel(DEBUG if debug else INFO)

set_debug()

def my_print(*args, **kwargs):
    log.info(" ".join(map(str, args)))
    if len(kwargs):
        print(*args, **kwargs)

def print_exc():
    with io.StringIO() as buf, open("logs/error_log.txt", "a") as f:
        traceback.print_exc(file=buf)
        f.write(buf.getvalue())