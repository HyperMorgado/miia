import logging
import sys

logger = logging.getLogger("mii_app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

import logging
from logging import Handler
import uuid
import os
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

# Environment configuration
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

class EnvironmentEnum:
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'

class TZFormatter(logging.Formatter):
    """
    Formatter that injects a timestamp in the specified timezone.
    """
    def __init__(self, fmt=None, datefmt=None, tz=ZoneInfo('America/Sao_Paulo')):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.tz = tz

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, self.tz)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

class Logger:
    """
    A Python logger mirroring the TypeScript Winston-based Logger.

    - Supports levels: critical, error, warning, info
    - Adds a console handler in all environments
    - Adds an email handler in production (requires mail_provider)
    - Allows registering default metadata for all log calls
    """
    def __init__(self, mail_provider=None, logger_id=None):
        self.mail_provider = mail_provider
        self.logger_id = logger_id or str(uuid.uuid4())
        self.default_metadata = {}

        # Create a native Python logger
        self._logger = logging.getLogger(self.logger_id)
        self._logger.setLevel(logging.DEBUG)

        # Common log format
        fmt = (
            '%(levelname)s %(asctime)s '  # Level and timestamp
            f'[{self.logger_id}][{ENVIRONMENT}] '  # Logger ID and env
            '%(message)s'  # The log message
            ' %(metadata)s'  # Serialized metadata
        )
        formatter = TZFormatter(fmt)

        # Console transport
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        # Email transport in production
        if ENVIRONMENT == EnvironmentEnum.PRODUCTION and mail_provider:
            mail_handler = MailHandler(mail_provider)
            mail_handler.setLevel(logging.ERROR)
            mail_handler.setFormatter(formatter)
            self._logger.addHandler(mail_handler)

    def register_metadata(self, payload: dict):
        """
        Merge provided payload into default metadata for future logs.
        """
        if payload:
            self.default_metadata.update(payload)

    def critical(self, message: str = '', metadata: dict = None, show_metadata: bool = True):
        self._log(logging.CRITICAL, message, metadata, show_metadata)

    def error(self, message: str = '', metadata: dict = None, show_metadata: bool = True):
        self._log(logging.ERROR, message, metadata, show_metadata)

    def warning(self, message: str = '', metadata: dict = None, show_metadata: bool = True):
        self._log(logging.WARNING, message, metadata, show_metadata)

    def info(self, message: str = '', metadata: dict = None, show_metadata: bool = True):
        self._log(logging.INFO, message, metadata, show_metadata)

    def _log(self, level: int, message: str, metadata: dict, show_metadata: bool):
        # Combine default metadata with call-specific metadata
        meta = self.default_metadata.copy()
        if metadata:
            meta.update(metadata)
        extra = {'metadata': meta if show_metadata else {}}
        self._logger.log(level, message, extra=extra)

class MailHandler(Handler):
    """
    Custom handler that sends emails via the provided mail_provider.

    mail_provider must implement a send_mail(to: list, subject: str, body: str) method.
    """
    def __init__(self, mail_provider):
        super().__init__()
        self.mail_provider = mail_provider

    def emit(self, record: logging.LogRecord):
        try:
            # Format the record to a string
            msg = self.format(record)
            # Example mail payload – adjust to your provider's API
            self.mail_provider.send_mail(
                to=["ops@example.com"],
                subject=f"Logger report - {ENVIRONMENT}",
                body=msg
            )
        except Exception:
            self.handleError(record)
