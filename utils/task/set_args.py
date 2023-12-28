import os
import argparse

from .model import Task
from ..log import Logmanager


def is_file_exists(file_path) -> bool:
    r = os.path.exists(file_path)
    if not r:
        LOGGER.error(f"文件{file_path}不存在")
    return r


def create_folder_if_not_exists(folder_path):
    if not folder_path:
        return
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def parse_command_line_args():
    """
    -c --config: 配置文件
    --log: 日志存放位置
    """
    parser = argparse.ArgumentParser(description="运行参数")

    parser.add_argument("--config", "-c", type=str, default="./config.ini", help="配置文件")
    parser.add_argument("--log", type=str, default="./", help="日志存放文件夹的位置,默认放到当前路径")
    args = parser.parse_args()

    # 初始化日志模块
    global LOGGER
    create_folder_if_not_exists(args.log)
    Logmanager(args.log)
    LOGGER = Logmanager.create_logger("CheckArgs")
    
    Task(args)
