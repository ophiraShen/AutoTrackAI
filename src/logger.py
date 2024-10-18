# src/logger.py
from loguru import logger
import sys

# 定义统一的日志格式字符串
log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}"

# 配置 Loguru，移除默认的日志配置
logger.remove()

# 使用统一的日志格式配置标准输出和标准错误输出，支持彩色显示
logger.add(sys.stdout, level="DEBUG", format=log_format, colorize=True)
logger.add(sys.stderr, level="ERROR", format=log_format, colorize=True)

# 使用统一的格式配置日志文件输出，设置文件大小为1MB，并进行轮转
logger.add("logs/app.log", rotation="1 MB", level="DEBUG", format=log_format)

# 为logger 这是别名
LOG = logger

# 将LOG 变量共开， 允许其它模块通过 from logger import LOG 导入
__all__ = ["LOG"]

