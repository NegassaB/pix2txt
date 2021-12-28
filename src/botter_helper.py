import sys
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
    # TEST_FILE = "pix/photo_2021-12-28_15-29-12.jpg"
    # print(api.ocr_file(open(TEST_FILE, 'rb')))
    return api.ocr_file(open(pic_location, 'rb'))
