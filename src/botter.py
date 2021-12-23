import enum
import logging
import time
import os
import sys

# 3rd party libs
from telethon import (
    TelegramClient,
    errors,
    events,
    Button
)
from telethon.tl.types import InputMessagesFilterPhotos
from dotenv import load_dotenv

# my own
from botter_helper import respond_error

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} pix2txt_bot.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# get logger
logger = logging.getLogger(__name__)

load_dotenv()

if not os.environ.get("API_ID"):
    respond_error("unable to get env API_ID")
if not os.environ.get("API_HASH"):
    respond_error("unable to get env API_HASH")
if not os.environ.get("TOKEN"):
    respond_error("unable to get env TOKEN")
else:
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    TOKEN = os.environ.get("TOKEN")


botter = TelegramClient('../pix2txt', API_ID, API_HASH).start(bot_token=TOKEN)

commands_dict = {
    'start_cmd': "/start",
    'help_cmd': "/help",
}

operation_status = dict()


class States(enum.Enum):
    START = enum.auto()
    RECV_PIC = enum.auto()

# todo: get pic from user
# todo: handle forwarded pix as well
# todo: store the image with some sort of id on the server
# todo: give image to ocrspace https://github.com/ErikBoesen/ocrspace/blob/master/example.py
# todo: return result as text & post to the group


@botter.on(events.NewMessage)
async def msg_event_handler(event):
    # todo: on start get user's telegram id
    # todo: insert into db perhaps
    user_id = event.sender_id
    if event.raw_text.lower() == "/start":
        await event.respond(
            f"hello {user_id} and welcome to pix2txt, please send the picture you wish to convert to text"
        )
        operation_status[user_id]['state'] = States.START
    elif event.photo:
        await event.reply("downloading and analyzing picture")
        operation_status[user_id]['state'] = States.RECV_PIC
    else:
        await event.reply("You have to /start the bot")


if __name__ == "__main__":
    with botter:
        try:
            botter.run_until_disconnected()
        except errors.FloodWaitError as fwe:
            logger.exception(f"hit flood wait error -- {fwe}, gotta sleep for {fwe.seconds}", exc_info=True)
            time.sleep(fwe.seconds)
            botter.run_until_disconnected()
        except errors.FloodError as fe:
            logger.exception(f"hit flood error -- {fe} with message -- {fe.message}", exc_info=True)
            time.sleep(5000)
            botter.run_until_disconnected()
        except Exception as e:
            logger.exception(f"unable to start bot -- {e}", exc_info=True)
            botter.run_until_disconnected()
        except KeyboardInterrupt:
            print("received EXITCMD, exiting")
            botter.disconnect()
            sys.exit(0)
