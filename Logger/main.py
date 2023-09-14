from loguru import logger
from loguru._logger import Logger
from pathlib import Path
import datetime, sys

# 路径设置
LOG_PATH = "logs"
# INFO显示模板
INFO_FORMAT_TEMPLATE = "<green>{time: YYYY/MM/DD HH:mm:ss}</green> <red>|</red> <green>{level}</green> <red>|</red> {message}"
# Warning显示模板
WARNING_FORMAT_TEMPLATE = "<green>{time: YYYY/MM/DD HH:mm:ss}</green> <red>|</red> <yellow>{level}</yellow> <red>|</red> {message}"
# ERROR显示模板
ERROR_FORMAT_TEMPLATE = "<green>{time: YYYY/MM/DD HH:mm:ss}</green> <red>|</red> <red>{level}</red> <red>|</red> {message}"
# 获取当前事件
DATE = datetime.datetime.now()

def level_filter(level: str):
    def is_level(record: dict):
        return record["level"].name == level
    return is_level


class LocalLogger:
    """ 日志封装 """

    def __init__(self) -> None:
        self.logger: Logger = logger.opt()
        # 调整logger设置
        self.logger.remove(0)
        self.__set_error_logger()
        self.__set_warning_logger()
        self.__set_success_logger()
        self.__set_info_logger()

    def __set_info_logger(self) -> None:
        """ 设置INFO日志配置 """
        # 日志文件名
        all_log_file_name = "all_logs-%s.log" % (DATE.strftime('%Y-%m-%d-%H_%M_%S'))
        all_log_file_path: Path = Path(__file__).parents[0].parents[0].resolve() / LOG_PATH / all_log_file_name
        # 添加日志配置
        self.logger.add(
            sink = all_log_file_path,
            format = INFO_FORMAT_TEMPLATE,
            level = "INFO"
        )

    def __set_success_logger(self) -> None:
        """ 设置SUCCESS日志配置 """
        # 添加日志配置
        self.logger.add(
            sink = sys.stderr,
            format = INFO_FORMAT_TEMPLATE,
            level = "SUCCESS",
            filter = level_filter(level = "SUCCESS")
        )

    def __set_warning_logger(self) -> None:
        """ 设置Warning日志配置 """
        # 添加日志配置
        self.logger.add(
            sink = sys.stderr,
            format = WARNING_FORMAT_TEMPLATE,
            level = "WARNING",
            filter = level_filter(level = "WARNING")
        )

    def __set_error_logger(self) -> None:
        """ 设置ERROR日志配置 """
        # 日志文件名
        err_log_file_name = "err_logs-%s.log" % (DATE.strftime('%Y-%m-%d-%H_%M_%S'))
        err_log_file_path: Path = Path(__file__).parents[0].parents[0].resolve() / LOG_PATH / err_log_file_name
        # 添加日志配置
        self.logger.add(
            sink = err_log_file_path,
            level = "ERROR",
            format = ERROR_FORMAT_TEMPLATE
        )