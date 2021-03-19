import atexit
import logging
import sys

import elasticsearch

from typing import Optional

addr: Optional[str] = None
ela = None


def init_elastic() -> None:
    global ela
    ela = elasticsearch.Elasticsearch(addr)


def init_addr() -> None:
    global addr
    addr = sys.argv[1]
    logging.info('Using address %s', addr)


def init_args() -> None:
    logging.info('Got args:')
    logging.info(sys.argv)

    init_addr()


def init_atexit() -> None:
    def end():
        logging.info('bye')

    atexit.register(end)


def init_logging() -> None:
    logging.basicConfig(
        format='ELASTIC-GRAB %(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info('hi')


def init() -> None:
    init_logging()
    init_atexit()
    init_args()


def main() -> None:
    init()


if __name__ == '__main__':
    main()
