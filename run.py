import os
import structlog

from transform import logger_status
logger = structlog.get_logger()


if __name__ == '__main__':
    logger.info(logger_status)
    logger.info('Starting SDX Transform-cs')
    # os.system("uvicorn app.routes:app --host 0.0.0.0 --port 5000 --workers 2")
    os.system("gunicorn transform:app -b :5000 -w 1 -k uvicorn.workers.UvicornWorker")
