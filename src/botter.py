import logging
import time
import sys

# 3rd party libs
from telethon import (
    TelegramClient,
    errors,
    events,
    Button
)

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} pix2txt_bot.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# get logger
logger = logging.getLogger(__name__)

api_id = None
api_hash = None
token = None

botter = TelegramClient('../pix2txt', api_id, api_hash).start(token)

# todo: get pic from user as inline
# todo: send to OCR library on server
# todo: return result as text & post to the group

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
