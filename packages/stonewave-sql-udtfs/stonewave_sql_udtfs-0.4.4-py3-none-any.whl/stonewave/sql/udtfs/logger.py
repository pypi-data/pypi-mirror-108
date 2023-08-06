import logging.config
import structlog
import os
import pathlib
from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
    merge_contextvars,
    unbind_contextvars,
)

LOG_LEVEL = os.getenv("SW_LOG_LEVEL") or "INFO"

log_file_dir = os.path.join(os.getenv("STONEWAVE_HOME", "/tmp"), "var", "logs", "py_table_funcs")
pathlib.Path(log_file_dir).mkdir(parents=True, exist_ok=True)
log_file = os.path.join(log_file_dir, "py_table_funcs.{}.log".format(os.getpid() % 1000))

timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
pre_chain = [
    # Add the log level and a timestamp to the event_dict if the log entry
    # is not from structlog.
    structlog.stdlib.add_log_level,
    timestamper,
]

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "plain": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=False),
                "foreign_pre_chain": pre_chain,
            },
        },
        "handlers": {
            "file": {
                "level": LOG_LEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_file,
                "formatter": "plain",
                "maxBytes": 2097152,  # 2MB
                "backupCount": 1,
            },
        },
        "loggers": {
            "": {
                "handlers": ["file"],
                "level": LOG_LEVEL,
                "propagate": True,
            },
        },
    }
)
structlog.configure(
    processors=[
        merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
bind_contextvars(pid=os.getpid())
