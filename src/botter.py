import logging
import time
import os
import sys

# 3rd party libs
from telethon import (
    TelegramClient,
    errors,
    events
)
from dotenv import load_dotenv

# my own
from botter_helper import (respond_error, convrt_return_txt, clean_up_pix)

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


@botter.on(events.NewMessage(incoming=True, pattern="/start"))
async def start_event_handler(event):
    user_id, user_name = await get_id_user_name(event)
    logger.info(f"user_id {user_id} user_name {user_name} has started the bot")
    await event.respond(f"hello **{user_name}** and welcome to pix2txt, please send a picture to extract the text.")


@botter.on(events.NewMessage(incoming=True, pattern="/help"))
async def help_event_handler(event):
    user_id, user_name = await get_id_user_name(event)
    logger.info(f"user_id {user_id} user_name {user_name} has clicked /help")
    await event.respond(
        "@pix2txt_bot can extract texts from pictures. "
        "__Just send a picture as you normally would and the bot will do the rest.__"
        "\n\nTo start using it, send /start and follow the directions provided by the bot."
        "\n\nUse /help to display this helpful message.\n\nIt only recognizes LATIN characters."
    )


async def check_content(event):
    user_id, user_name = await get_id_user_name(event)
    logger.info(f"checking if user_id {user_id} user_name {user_name} sent a picture")
    if event.photo:
        return True
    elif event.raw_text.lower() == "/start":
        return False
    elif event.raw_text.lower() == "/help":
        return False
    else:
        await event.reply(
            f"**{user_name}** you sent an __Unknown command__, please use the provided commands,"
            "if you are experiencing difficulties using the bot press /help"
        )
        return False


@botter.on(events.NewMessage(incoming=True, func=check_content))
async def pic_event_handler(event):
    user_id, user_name = await get_id_user_name(event)
    logger.info(f"checking if user_id {user_id} user_name {user_name} did send a picture")
    pic_file = await botter.download_media(event.photo, file="pix/")
    logger.info(f"downloading picture sent by user_id {user_id} user_name {user_name}")
    if not pic_file:
        logger.warning(f"user_id {user_id} user_name {user_name} didn't send a proper picture")
        await event.reply("Please send a picture file you wish to convert to text, nothing else")
        await event.delete()
    else:
        logger.info(f"user_id {user_id} user_name {user_name} has sent a proper picture")
        loading_gif = await event.reply("downloading and analyzing picture, PLEASE WAIT", file='loading.gif')
        logger.info(f"sent loading_gif to user_id {user_id} user_name {user_name}")
        await event.reply(convrt_return_txt(pic_file))
        await loading_gif.delete()
        logger.info(f"successfully sent extracted text to user_id {user_id} user_name {user_name}")
        clean_up_pix(pic_file)
        logger.info(f"user_id {user_id} user_name {user_name} is done")


async def get_id_user_name(event):
    user_id, user_name = None, None
    logger.info(f"extracting user_id and user_name from event")
    if event.chat.username:
        logger.info(f"username exists {event.chat.username}")
        user_name = event.chat.username
    elif event.chat.first_name:
        logger.info(f"username DOESN'T exists, using first_name instead {event.chat.first_name}")
        user_name = event.chat.first_name
    else:
        logger.info(f"neither username nor first_name exist, using unknown username instead")
        user_name = "unknown username"
    user_id = event.sender_id
    logger.info(f"successfully retrieved user_id {user_id} and user_name {user_name}")
    return user_id, user_name


if __name__ == "__main__":
    with botter:
        logger.info(f"starting the bot")
        try:
            botter.run_until_disconnected()
        except errors.FloodWaitError as fwe:
            logger.exception(f"hit flood wait error -- {fwe}, gotta sleep for {fwe.seconds}", exc_info=True)
            time.sleep(fwe.seconds)
            logger.info(f"attempting to re-start the bot")
            botter.run_until_disconnected()
        except errors.FloodError as fe:
            logger.exception(f"hit flood error -- {fe} with message -- {fe.message}", exc_info=True)
            time.sleep(5000)
            logger.info(f"attempting to re-start the bot")
            botter.run_until_disconnected()
        except Exception as e:
            logger.exception(f"unable to start bot -- {e}", exc_info=True)
            logger.info(f"attempting to re-start the bot")
            botter.run_until_disconnected()
        except KeyboardInterrupt:
            logger.warning(f"received EXITCMD, exiting")
            botter.disconnect()
            logger.info(f"bot disconnected, closing bot script")
            sys.exit(0)
        else:
            logger.info(f"successfully started the bot, starting operations")
