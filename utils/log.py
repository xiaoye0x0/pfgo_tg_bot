import logging
import threading
from logging.handlers import RotatingFileHandler

from .base import SingletonMeta


class Logmanager(metaclass=SingletonMeta):
    log_list = []
    log_list_lock = threading.Lock()
    path = "./"

    def __init__(self, path: str) -> None:
        Logmanager.path = path

    @classmethod
    def create_logger(cls, name=None):
        if name is None:
            name = "default"
        logger = logging.getLogger(name)
        if name not in cls.log_list:
            with Logmanager.log_list_lock:
                if name not in cls.log_list:
                    cls.log_list.append(name)
                    logger.setLevel(logging.INFO)
                    logfile = f"{Logmanager.path}/log.log"
                    fh = RotatingFileHandler(
                        logfile,
                        mode="a",
                        maxBytes=1024 * 1024 * 10,
                        backupCount=2,
                        encoding="utf-8",
                    )
                    formatter = logging.Formatter(
                        "[%(name)s] [%(asctime)s] [%(levelname)s] %(message)s",
                        "%Y%m%d-%H:%M:%S",
                    )
                    fh.setFormatter(formatter)
                    logger.addHandler(fh)

                    ch = logging.StreamHandler()
                    ch.setFormatter(formatter)
                    logger.addHandler(ch)
                    fh.close()
                    ch.close()
        return logger
