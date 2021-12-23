import sys
import logging

# enable logging
logging.basicConfig(
    # filename=f"log {__name__} pix2txt_bot.log",
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# get logger
logger = logging.getLogger(__name__)


def respond_error(error_details):
    logger.error("{error_details}", exc_info=True)
    sys.exit(1)
