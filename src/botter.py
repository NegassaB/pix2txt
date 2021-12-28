import asyncio
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
from botter_helper import (respond_error, convrt_return_txt)

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
    'convert_pic': "/convert_pic",
}

operation_status = dict()


class States(enum.Enum):
    START = enum.auto()
    RECV_PIC = enum.auto()
    AWAIT_RESULT = enum.auto()
    END = enum.auto()

# hack: handle forwarded pix as well
# todo: clean up operation in the pix folder


@botter.on(events.NewMessage)
async def msg_event_handler(event):
    user_id = event.sender_id
    if event.raw_text.lower() == commands_dict['start_cmd']:
        await event.respond(
            f"hello {user_id} and welcome to pix2txt, please send /convert_pic"
        )
        operation_status[user_id] = {'state': States.START}
    elif event.raw_text.lower() == commands_dict['help_cmd']:
        await event.respond(
            "@pix2txt_bot can extract texts from pictures. To start using it, send /start "\
            "and follow the directions provided by the bot. Use /help to display this helpful message."
        )
    elif user_id in operation_status.keys():
        current_state = operation_status[user_id]['state']
        if event.raw_text.lower() == commands_dict['convert_pic']:
            await event.reply("Please send the picture you wish to convert to text")
            operation_status[user_id]['state'] = States.RECV_PIC
        elif current_state == States.RECV_PIC:
            if event.photo:
                operation_status[user_id]['state'] = States.AWAIT_RESULT
                pic_file = await botter.download_media(event.photo, file="pix/")
                if not pic_file:
                    await event.reply("Please send a picture file you wish to convert to text, nothing else")
                    await event.delete()
                    operation_status[user_id]['state'] = States.RECV_PIC
                else:
                    loading_gif = await event.reply("downloading and analyzing picture, PLEASE WAIT", file='loading.gif')
                    await event.reply(convrt_return_txt(pic_file))
                    await loading_gif.delete()
                    operation_status[user_id]['state'] = States.END
                    await event.respond("Done and Good Bye, if you want to use the bot again press /start")
            else:
                await event.reply("Please send a picture file, nothing else")
                await event.delete()
                operation_status[user_id]['state'] == States.RECV_PIC
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
