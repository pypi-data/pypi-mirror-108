import logging
import typing
from logging import LogRecord


__all__ = ["DiscordFormatter"]

LEVEL_TO_EMOJI = {
    logging.DEBUG: "white_check_mark",
    logging.INFO: "information_source",
    logging.WARNING: "warning",
    logging.ERROR: "bangbang",
    logging.CRITICAL: "bangbang",
}


class DiscordFormatter(logging.Formatter):
    def __init__(self, user_id_to_alert: typing.Optional[str] = None):
        self.user_id_to_alert = user_id_to_alert

    def format(self, record: LogRecord) -> str:
        return (
            f":{LEVEL_TO_EMOJI[record.levelno]}: **{record.levelname}**{f' <@{self.user_id_to_alert}>'if record.levelno >= logging.ERROR else ''}\n"
            f">>> {record.msg}"
        )
