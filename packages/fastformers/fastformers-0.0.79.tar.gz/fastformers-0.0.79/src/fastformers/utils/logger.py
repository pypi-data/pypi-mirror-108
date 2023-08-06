from typing import Optional

import sys
import logging
import datetime


class ExactTimeFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(fmt='%(asctime)s\t%(message)s', datefmt='%H:%M:%S')

    def formatTime(self, record, datefmt: Optional[str] = None):
        cur_t = datetime.datetime.fromtimestamp(record.created)
        return f'{cur_t.strftime(self.default_time_format if datefmt is None else datefmt)}.' \
               f'{cur_t.microsecond // 1000:04d}'


def init_logger():
    service_logger = logging.getLogger('fastformers')
    service_logger.propagate = False
    service_logger.setLevel(logging.DEBUG)
    if service_logger.handlers:
        return service_logger

    # create and set formatting for the logging file handler
    fh = logging.StreamHandler(sys.stdout)
    fh.setFormatter(ExactTimeFormatter())

    # add handler to logger object
    service_logger.addHandler(fh)
    return service_logger


logger = init_logger()
