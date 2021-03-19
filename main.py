import atexit
import json
import logging
import sys

import elasticsearch

from typing import Optional

addr: Optional[str] = None
ela: Optional[elasticsearch.Elasticsearch] = None


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
        Init.PrivateInit.init_elastic()


def query():
    resp = ela.search(index='_all', size=10000, scroll='1m', pretty=True)
    old_scroll_id = resp['_scroll_id']
    payload = []

    while len(resp['hits']['hits']):
        payload.append(resp['hits']['hits'])

        resp = ela.scroll(
            scroll_id=old_scroll_id,
            pretty=True,
            scroll='1m'  # length of time to keep search context
        )

        if old_scroll_id != resp['_scroll_id']:
            logging.info("NEW SCROLL ID: %s", resp['_scroll_id'])

        # keep track of pass scroll _id
        old_scroll_id = resp['_scroll_id']

    return payload


def write_loads(loads) -> None:
    for i in range(len(loads)):
        obj = loads[i]
        file_name = f'{i}.json'
        fp = open(file_name, 'w')

        json.dump(obj, fp, indent=4, sort_keys=True)
        fp.close()


def main() -> None:
    Init.init()
    load = query()
    write_loads(load)


if __name__ == '__main__':
    main()
