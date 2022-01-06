import structlog

from transform import app
from waitress import serve

logger = structlog.get_logger()


if __name__ == '__main__':
    logger.info('Starting SDX Transform')
    serve(app, host='0.0.0.0', port=5000)
