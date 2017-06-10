#!/usr/bin/env python
import argparse
import time
from collections import OrderedDict


def setup():
    time.sleep(10)
    print("setup complete")


def compile():
    time.sleep(20)
    print("compile complete")


def test():
    time.sleep(30)
    print("test complete")


def package():
    time.sleep(40)
    print("package complete")


steps = OrderedDict([
    ('setup', setup),
    ('compile', compile),
    ('test', test),
    ('package', package),
])


def hello():
    print("\n".join(steps.keys()))

parser = argparse.ArgumentParser(description='Build it')
parser.add_argument('--list_steps', action='store_true')
parser.add_argument('--run', nargs=1)

args = parser.parse_args()

if args.list_steps:
    hello()

if args.run:
    action = args.run[0]
    steps[action]()
