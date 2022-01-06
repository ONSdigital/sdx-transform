import sys
import structlog

from transform import app
from waitress import serve

logger = structlog.get_logger()


class ErrorFilter:

    def __init__(self):
        self.stderr = sys.stderr

    def __getattr__(self, attr_name):
        return getattr(self.stderr, attr_name)

    def write(self, data):
        if ' [INFO] ' not in data:
            self.stderr.write(data)
            self.stderr.flush()
        else:
            sys.stdout.write(data)
            sys.stdout.flush()

    def flush(self):
        self.stderr.flush()


if __name__ == '__main__':
    logger.info('Starting SDX Transform')
    sys.stderr = ErrorFilter()
    serve(app, host='0.0.0.0', port=5000)
