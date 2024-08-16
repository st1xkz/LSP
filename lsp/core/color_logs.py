import logging


FORMATS = {
    logging.DEBUG: (
        "[1;38;2;242;202;80m[{levelname}][0m "
        "[38;2;242;202;80m{name}: {message}[0m"
    ),
    logging.INFO: (
        "[1;38;2;33;64;61m[{levelname}][0m " "[38;2;33;64;61m{name}: {message}[0m"
    ),
    logging.WARNING: (
        "[1;38;2;45;95;115m[{levelname}][0m " "[38;2;45;95;115m{name}: {message}[0m"
    ),
    logging.ERROR: (
        "[1;38;2;184;127;222m[{levelname}][0m "
        "[38;2;184;127;222m{name}: {message}[0m"
    ),
    logging.CRITICAL: (
        "[1;38;2;109;77;140m[{levelname}][0m "
        "[38;2;109;77;140m{name}: {message}[0m"
    ),
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS.get(record.levelno, "{levelname} {name}: {message}")
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)


handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[handler],
)

log = logging.getLogger("colored-logger")
log.debug("DEBUG MESSAGE")
log.info("INFO MESSAGE")
log.warning("WARNING MESSAGE")
log.error("ERROR MESSAGE")
log.critical("CRITICAL MESSAGE")
