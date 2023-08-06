__all__ = ["DiscordFormatter"]

import logging
import typing
import traceback
from logging import LogRecord


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
        header = f":{LEVEL_TO_EMOJI[record.levelno]}: **{record.levelname}**"
        if record.levelno >= logging.ERROR:
            header += f" <@{self.user_id_to_alert}>"

        header += '\n'

        body = f"> {record.msg}\n"

        if record.exc_info:
            _, exc, _ = record.exc_info
            body += f"```{traceback.format_exc()}```"

        return header + body
