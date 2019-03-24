import logging

FORMAT = "%(relativeCreated)5d %(asctime)s %(name)-15s %(levelname)-8s %(message)s"
IS_INITIALIZED = False

ROOT = logging.getLogger("root")


def _prepare_handler(handler: logging.Handler, level: int = None, fmt: str = None) -> logging.Handler:
    handler.setLevel(level or logging.DEBUG)
    handler.setFormatter(logging.Formatter(fmt or FORMAT))
    return handler


def init(*, level: int = None, fmt: str = None, console: bool = True, file: str = None, ):
    global ROOT, IS_INITIALIZED

    if not IS_INITIALIZED:
        level = level or logging.DEBUG
        ROOT.setLevel(level)

        if console:
            ROOT.addHandler(_prepare_handler(logging.StreamHandler(), level, fmt))

        if file:
            ROOT.addHandler(_prepare_handler(logging.FileHandler(file), level, fmt))

        IS_INITIALIZED = True


def debug(msg, *args, **kwargs):
    ROOT.debug(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    ROOT.error(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    ROOT.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    ROOT.warning(msg, *args, **kwargs)
