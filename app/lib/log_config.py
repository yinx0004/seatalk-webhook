LOG_LEVEL: str = "DEBUG"
logging_config = {
    "version": 1,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "%(levelprefix)s %(name)s | %(asctime)s | %(filename)s | %(funcName)s() | line %(lineno)d | %(message)s",
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "format": "%(levelprefix)s %(name)s | %(asctime)s | %(client_addr)s | %(request_line)s %(status_code)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "default": {"handlers": ["default"],
                    "level": LOG_LEVEL,
                    "propagate": False
                    },
        "uvicorn.error": {"level": LOG_LEVEL},
        "uvicorn.access": {
            "handlers": ["access"],
            "level": LOG_LEVEL,
            "propagate": False
        }
    },
}
