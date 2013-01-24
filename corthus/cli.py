#!/usr/bin/python

import argparse
import sys
import os.path
import shlex

current_dir = None

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
        return self.val

class Command():
    def run(self, cli_args):
        args_dict = vars(self.parser.parse(cli_args))
        print self.fun.func_name + ' ' + args_dict
        self.fun(**args_dict)

if __name__ == '__main__':

    from toolkit.TextFolder import TextFolder

    current_dir = sys.argv[1]
    current_ptext = TextFolder(current_dir)

    # this follows function signetures from TextFolder class
    ps = {}
    ps['show'] = argparse.ArgumentParser(description='Show a text or alignment.')
    ps['show'].add_argument('langs', metavar='lang', nargs='+', type=lang)
    ps['align'] = argparse.ArgumentParser(description='Align 2 texts.')
    ps['align'].add_argument('lang1')
    ps['align'].add_argument('lang2')
#    ps['align'].add_argument('--plot', action="store_true", default=False,
#                             help='plots the cost table to plot.png')
#    ps['align'].add_argument('--text', action="store_true", default=False,
#                             help='shows the alignment as pretty-printed text')
    ps['align'].add_argument('--no-hand', action="store_true", default=None,
                             help='use file with hand-aligned sentence pairs')

    for i in range(1):
        try:
#            line = raw_input('\x1b[0;36m' + current_ptext.name + '>\x1b[0m ') # with readline
#            cmd = shlex.split(line) # command as a list
            cmd = sys.argv[2:]
            print cmd
            if not cmd:
                continue
            elif cmd[0] == 'help':
                try:
                    ps[cmd[1]].print_help()
                except:
                    print 'Commands: ' + ', '.join(ps)
                    print 'Type: <command> --help to get help about a specific command.'
                    print __doc__
            elif cmd[0] in ps:
                try:
                    args = ps[cmd[0]].parse_args(cmd[1:])
                except SystemExit: # occurs on '--help':
                    continue
                # calling specified method on current_ptext
                print args
                getattr(current_ptext, cmd[0]).__call__(**vars(args))
            else:
                print 'Unknown command ' + cmd[0] + '.'
        except EOFError:
            print 'EOF, exiting'
            raise SystemExit





raise SystemExit

################# old rl.py

from textwrap import wrap

readline.read_init_file()
readline.parse_and_bind("TAB: history-search-backward")
readline.parse_and_bind("ESC: kill-line")
