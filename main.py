import atexit
import logging
import sys

import elasticsearch

from typing import Optional

addr: Optional[str] = None
ela = None


class Init:
    class PrivateInit:
        @staticmethod
        def init_elastic() -> None:
            global ela
            ela = elasticsearch.Elasticsearch(addr)

        @staticmethod
        def init_addr() -> None:
            global addr
            addr = sys.argv[1]
            logging.info('Using address %s', addr)

        @staticmethod
        def init_args() -> None:
            logging.info('Got args:')
            logging.info(sys.argv)

            Init.PrivateInit.init_addr()

        @staticmethod
        def init_atexit() -> None:
            def end():
                logging.info('bye')

            atexit.register(end)

        @staticmethod
        def init_logging() -> None:
            logging.basicConfig(
                format='ELASTIC-GRAB %(asctime)s %(levelname)-8s %(message)s',
                level=logging.INFO,
                datefmt='%Y-%m-%d %H:%M:%S')

            logging.info('hi')

    @staticmethod
    def init() -> None:
        Init.PrivateInit.init_logging()
        Init.PrivateInit.init_atexit()
        Init.PrivateInit.init_args()


def main() -> None:
    Init.init()


if __name__ == '__main__':
    main()
