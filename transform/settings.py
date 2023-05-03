import os

from sdx_gcp.app import get_logger, SdxApp


logger = get_logger()


def _get_value(key, default_value=None):
    """Gets a value from an environment variable , will use default if present else raise a value Error
    """
    value = os.getenv(key, default_value)
    if not value:
        logger.error("No value set for {}".format(key))
        raise ValueError()
    return value


PROJECT_ID = os.getenv('PROJECT_ID')

FTP_PATH = "\\"
SDX_FTP_IMAGE_PATH = _get_value("SDX_FTP_IMAGES_PATH", "EDC_QImages")

SDX_FTP_DATA_PATH = "EDC_QData"
SDX_FTP_RECEIPT_PATH = "EDC_QReceipts"
SDX_RESPONSE_JSON_PATH = "EDC_QJson"

USE_IMAGE_SERVICE: bool = os.getenv('USE_IMAGE_SERVICE', "false") == "true"

sdx_app = SdxApp("sdx-survey", PROJECT_ID)


def cloud_config():
    global FTP_PATH
    FTP_PATH = sdx_app.secrets_get("ftp-path")[0]
