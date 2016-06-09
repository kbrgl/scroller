import time
import argparse
import config
import sys
import select
import signal

signal.signal(signal.SIGPIPE, signal.SIG_DFL)


class InputReceived(Exception):
    pass

parser = argparse.ArgumentParser(description=config.description)

parser.add_argument(
                    '-i', '--interval',
                    dest='interval',
                    default=0.2,
                    type=float,
                    help='specify scroll speed in seconds'
                   )

parser.add_argument(
                    '-n', '--newline',
                    action='store_true',
                    default=False,
                    dest='newline',
                    help='print each permutation on a separate line'
                   )

parser.add_argument(
                    '-s', '--separator',
                    dest='sep',
                    default=' ',
                    help='append a separator to input string before animating, \
                            used as padding'
                   )

parser.add_argument(
                    '-l', '--length',
                    dest='len',
                    type=int,
                    default=0,
                    help='scroll text only if its length is greater than or \
                            equal to this value'
                   )

parser.add_argument(
                    '-c', '--count',
                    dest='count',
                    type=int,
                    help='specify number of characters to scroll'
                   )

parser.add_argument(
                    '-r', '--reverse',
                    dest='reverse',
                    default=False,
                    action='store_true',
                    help='scroll text in the opposite direction'
                   )

parser.add_argument(
                    '-o', '--open',
                    dest='open',
                    default=False,
                    action='store_true',
                    help='keep stdin open and reload on any new input'
                   )

parser.add_argument(
                    '-p', '--persist',
                    dest='persist',
                    default=False,
                    action='store_true',
                    help='if using --open flag, \
                            do not exit after stdin is closed'
                   )

parser.add_argument(
                    '-v', '--version',
                    dest='version',
                    default=False,
                    action='store_true',
                    help='print version and exit'
                   )


def permute(string, rev=False):
    return (string[-1] + string[:-1] if rev else string[1:] + string[0])


def scroll(string, rev=False, sep='', static=False):
    string = string + sep
    if static:
        while True:
            yield string
    else:
        while True:
            string = permute(string, rev=rev)
            yield string


def scroller(string,
             static=False, count=float('inf'),
             rev=False, sep=''):
    for i, permutation in enumerate(scroll(string,
                                           rev=rev,
                                           sep=sep,
                                           static=static)):
        if i >= count:
            break
        yield permutation


def main(string=None, args=None):
    if args is None:
        args = parser.parse_args()

    if args.version:
        print("Scroller {}".format(config.version))
        return

    if string is None:
        try:
            string = input()
        except KeyboardInterrupt:
            print(end='\r')
            return

    static = False
    if args.len >= len(string):
        static = True

    end = '\r'
    if args.newline:
        end = '\n'

    interval = args.interval
    if args.interval < 0:
        interval = 0.2

    count = float('inf')
    if args.count and args.count >= 0:
        count = args.count

    try:
        if not args.open:
            for permutation in scroller(string,
                                        static,
                                        count,
                                        args.reverse,
                                        args.sep):
                if args.len:
                    permutation = permutation[:args.len + 1]
                print(permutation, end=end)
                sys.stdout.flush()
                time.sleep(interval)
        else:
            try:
                for permutation in scroller(string,
                                            static,
                                            count,
                                            args.reverse,
                                            args.sep):
                    r, _, _ = select.select([sys.stdin], [], [], 0)
                    if sys.stdin in r:
                        raise InputReceived
                    if args.len:
                        permutation = permutation[:args.len - 1]
                    print(permutation, end=end)
                    sys.stdout.flush()
                    time.sleep(interval)
            except InputReceived:
                try:
                    string = input()
                except EOFError:
                    if args.persist:
                        args.open = False
                        main(string, args)
                    else:
                        return
                if not args.newline:
                    sys.stdout.write('\033[K')
                main(string, args)

    except KeyboardInterrupt:
        print(end='\r')


if __name__ == '__main__':
    main()
