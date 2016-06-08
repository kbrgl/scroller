#!/usr/bin/env python3
import time
import argparse
import config
import sys
import select

parser = argparse.ArgumentParser(description=config.description)
parser.add_argument('-i', '--interval', dest='interval', default=0.2, type=float, help='specify scroll speed in seconds')
parser.add_argument('-n', '--newline', action='store_true', default=False, dest='newline', help='print each permutation on a separate line')
parser.add_argument('-s', '--separator', dest='sep', default=' ', help='append a separator to input string before animating, used as padding')
parser.add_argument('-l', '--length', dest='len', type=int, default=0, help='scroll text only if its length is greater than or equal to this value')
parser.add_argument('-c', '--count', dest='count', type=int, help='specify number of characters to scroll')
parser.add_argument('-r', '--reverse', dest='reverse', default=False, action='store_true', help='scroll text in the opposite direction')

def permute(string, rev=False):
    return (string[-1] + string[:-1] if rev else string[1:] + string[0])

def scroll(string, rev=False, sep='', static=False):
    string = string + sep
    while True:
        if not static:
            string = permute(string, rev=rev)
        yield string

def scroller(string,
         static=False, count=float('inf'),
         reverse=False, sep=''):
    for i, permutation in enumerate(scroll(string, rev=reverse, sep=sep, static=static)):
        if i >= count:
            break
        yield permutation

def main(string=None, args=None):
    if args is None:
        args = parser.parse_args()

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
        for permutation in scroller(string, static, count, args.reverse, args.sep):
            print(permutation, end=end)
            time.sleep(interval)

    except KeyboardInterrupt:
        print(end='\r')


if __name__ == '__main__':
    main()
