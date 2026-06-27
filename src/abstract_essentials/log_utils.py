"""
abstract_essentials.log_utils
================================
Rotating-file logger factory with per-logger level filtering.
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

_PACKAGE_NAME = "abstract_essentials"

LOG_FORMAT = (
    "[%(asctime)s] "
    "%(levelname)-8s "
    "%(name)s:%(lineno)d | "
    "%(message)s "
    "[target=%(target_file)s:%(target_line)s]"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class LevelFilter(logging.Filter):
    """Filter that allows selective per-level enablement / disablement."""

    def __init__(self):
        super().__init__()
        self.enabled_levels = {
            logging.DEBUG, logging.INFO, logging.WARNING,
            logging.ERROR, logging.CRITICAL,
        }

    def filter(self, record):
        return record.levelno in self.enabled_levels

    def enable_level(self, level):
        self.enabled_levels.add(level)

    def disable_level(self, level):
        self.enabled_levels.discard(level)

    def is_enabled(self, level):
        return level in self.enabled_levels


class SafeFormatter(logging.Formatter):
    """Formatter that tolerates missing ``target_*`` extra fields."""

    def format(self, record):
        record.target_file = getattr(record, "target_file", "-")
        record.target_line = getattr(record, "target_line", "-")
        return super().format(record)


def _resolve_log_root():
    """Return the best writable log directory, falling back through /tmp."""
    venv = os.getenv("VIRTUAL_ENV") or os.getenv("CONDA_PREFIX")
    if venv:
        p = os.path.join(venv, ".logs", _PACKAGE_NAME)
        os.makedirs(p, exist_ok=True)
        return p

    home = os.path.join(os.path.expanduser("~"), ".cache", _PACKAGE_NAME, "logs")
    try:
        os.makedirs(home, exist_ok=True)
        return home
    except PermissionError:
        pass

    try:
        syslog = os.path.join("/var/log", _PACKAGE_NAME)
        os.makedirs(syslog, exist_ok=True)
        return syslog
    except PermissionError:
        fallback = os.path.join("/tmp", _PACKAGE_NAME, "logs")
        os.makedirs(fallback, exist_ok=True)
        return fallback


LOG_ROOT = _resolve_log_root()

# Per-logger LevelFilter instances for runtime control.
_level_filters = {}


def get_logFile(name, *, level=logging.INFO, console=True,
                max_bytes=5 * 1024 * 1024, backup_count=5):
    """
    Return a configured rotating-file logger named *name*.

    Writes to ``LOG_ROOT/<name>.log`` and optionally the console.
    Uses SafeFormatter and a per-logger LevelFilter.
    Re-uses an already-configured logger without re-initialising.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    formatter = SafeFormatter(LOG_FORMAT, DATE_FORMAT)

    level_filter = LevelFilter()
    if level > logging.DEBUG:
        level_filter.disable_level(logging.DEBUG)
    _level_filters[name] = level_filter

    log_path = os.path.join(LOG_ROOT, f"{name}.log")
    try:
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        file_handler.addFilter(level_filter)
        logger.addHandler(file_handler)
    except PermissionError:
        logger.addHandler(logging.NullHandler())

    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        console_handler.addFilter(level_filter)
        logger.addHandler(console_handler)

    logger.propagate = False
    return logger


__all__ = [
    "LevelFilter", "SafeFormatter", "get_logFile",
    "LOG_FORMAT", "DATE_FORMAT", "LOG_ROOT",
]
