__all__ = ["DiscordWebhookHandler"]
import logging
from logging import LogRecord

import requests


class DiscordWebhookHandler(logging.Handler):
    def __init__(self, webhook_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.webhook_url = webhook_url

    def emit(self, record: LogRecord) -> None:
        requests.post(self.webhook_url, json={"content": self.format(record)})
