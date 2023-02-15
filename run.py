import structlog

from transform import app
from waitress import serve

from transform.settings import cloud_config

logger = structlog.get_logger()


if __name__ == '__main__':
    logger.info('Starting SDX Transform')
    cloud_config()
    serve(app, host='0.0.0.0', port=5000)
