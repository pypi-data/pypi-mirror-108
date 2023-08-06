#!/usr/bin/env python3

"""
Nagios/icinga plugin for checking a RQ redis queues.

Author: Crafter B.V.
License: MIT
"""

import argparse
import nagiosplugin
from rq import Queue
from redis import Redis


class CheckRQ(nagiosplugin.Resource):
    def __init__(self,
                 db=0,
                 queue='default',
                 host='localhost',
                 port=6379,
                 password='',
                 ):
        self.queue_name = queue
        self.host = host
        self.db = db
        self.port = port
        self.password = password

    def probe(self):
        connection = Redis(host=self.host, port=self.port,
                           db=self.db, password=self.password)
        queue = Queue(self.queue_name, connection=connection)

        queue_length = len(queue)

        return [nagiosplugin.Metric(
            'queue_length', int(queue_length), context='queue_length', min=0)]


def main():
    parser = argparse.ArgumentParser(
        __file__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('Nagios/icinga plugin for checking a RQ redis queues'),
    )

    parser.add_argument('--queue', dest='queue',
                        help='RQ Queue', default='default')

    parser.add_argument('--db', dest='db',
                        help='Redis Database', default='0')

    parser.add_argument('--host', dest='host',
                        help='Redis host', default='localhost')

    parser.add_argument('--port', dest='port',
                        help='Redis port', default=6379)

    parser.add_argument('--password', dest='password',
                        help='Redis password', default='')

    parser.add_argument('-w', '--warn', dest='warning',
                        help='WARNING trigger', default='10')

    parser.add_argument('-c', '--critical', dest="critical",
                        help='CRITICAL triger', default='20')

    parser.add_argument('-v', '--version', help='Print version',
                        action='version', version='%(prog)s 0.1.5')

    args = parser.parse_args()

    check = nagiosplugin.Check(
        CheckRQ(
            db=args.db,
            queue=args.queue,
            host=args.host,
            port=args.port,
            password=args.password,
        ),
        nagiosplugin.ScalarContext('queue_length', args.warning, args.critical)
    )
    check.main()


if __name__ == '__main__':
    main()
