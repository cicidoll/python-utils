from loguru._logger import Logger
from .main import LocalLogger

logger: Logger = LocalLogger().logger