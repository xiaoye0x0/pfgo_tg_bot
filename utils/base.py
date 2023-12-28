import sys
import traceback

from logging import Logger


class SingletonMeta(type):
    """单例"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def catch_exception(logger: Logger, exception_message: str, exist: bool = False):
    """异常捕获装饰器"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except:
                logger.error(f"{exception_message}: {traceback.format_exc()}")
                if exist:
                    sys.exit()

        return wrapper

    return decorator


def str_in_list_str(target: str, target_list: list) -> bool:
    """检测字符串中是否存在list中字符串"""
    for target_str in target_list:
        if target_str in target:
            return True
    return False
