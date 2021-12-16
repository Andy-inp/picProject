import sys, os
import logging
import logging.config
import logging.handlers
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取日志器
class GetLogger:
    _logger = ["root", "basiclogger", "smmslogger"]
    def __init__(self, logpath=None):
        self.logpath = logpath if logpath else f"{BASE_DIR}/config/logger.yaml"

    def get_logger(self, logger="basiclogger") -> "return init logger":
        if logger in self._logger:
            logging.config.fileConfig(self.logpath)
            return logging.getLogger(logger)
        else:
            raise ValueError(f"选择的日志器未在配置中找到，请检查日志配置文件{self.logpath}")
