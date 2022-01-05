import sys

import structlog
from transform import app
from waitress import serve


logger = structlog.get_logger()


# class Server(BaseApplication):
#
#     def __init__(self, application, options_dict=None):
#         self.options = options_dict or {}
#         self.application = application
#         super().__init__()
#
#     def load_config(self):
#         config = {key: value for key, value in self.options.items()
#                   if key in self.cfg.settings and value is not None}
#         for key, value in config.items():
#             self.cfg.set(key.lower(), value)
#
#     def load(self):
#         return self.application


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
