#!/usr/bin/python

import argparse
import sys

class lang(object):
    def __init__(self, arg):
        langs_allowed = ('pl', 'cu', 'el')
        if isinstance(arg, lang):
            self.val = arg.val
        elif arg in langs_allowed:
            self.val = arg
        else:
            raise ValueError

    def __str__(self):
        return '<lang: ' + self.val + '>'

class inputText

parser = argparse.ArgumentParser(description='sum the integers at the command line')
parser.add_argument('integers', metavar='foo', nargs='+', type=lang,
                    help='an integer to be summed')
parser.add_argument('--log', default=sys.stdout, type=argparse.FileType('w'),
                    help='the file where the sum should be written')
args = parser.parse_args()

#args.log.write('%s' % sum(args.integers))
#args.log.close()
