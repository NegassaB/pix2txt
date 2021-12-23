import logging
import unittest

# 3rd party libs
from telethon import (
    TelegramClient,
    errors,
    events,
    Button
)
from telethon.tl.custom.message import Message

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} pix2txt_bot.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# get logger
logger = logging.getLogger(__name__)


class BotterTestSuite(unittest.TestCase):

    def setUp(self):
        pass

    def test_01start_bot():
        pass
