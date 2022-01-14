import sys
import os
import logging

# 3rd party libs
import ocrspace

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} pix2txt_bot.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# get logger
logger = logging.getLogger(__name__)

api = ocrspace.API()


def respond_error(error_details):
    logger.error(f"{error_details}", exc_info=True)
    sys.exit(1)


def convrt_return_txt(pic_location):
    logger.info(f"extracting text from picture")
    try:
        output = api.ocr_file(open(pic_location, 'rb'))
    except Exception as e:
        logger.error(f"unable to extract text from picture -- {e}", exc_info=True)
        return "SOMETHING WENT WRONG, PLEASE TRY AGAIN"
    else:
        if output:
            logger.info(f"successfully extracted text from picture, returning result to bot")
            return output
        else:
            logger.error(f"The OUTPUT is None -- {output}, something definitely went wrong", exc_info=True)
            return "SOMETHING WENT WRONG, PLEASE TRY AGAIN"
    finally:
        clean_up_pix(pic_location)


def clean_up_pix(picture_file):
    logger.info("attempting to delete picture file from server")
    try:
        os.remove(picture_file)
    except Exception as e:
        logger.error(f"unable to delete pic file -- {e}", exc_info=True)
    else:
        logger.info(f"successfully delete pic file {picture_file}")
    finally:
        return
