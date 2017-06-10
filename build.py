#!/usr/bin/env python
import argparse
from collections import OrderedDict


def setup():
    print("setup complete")


def compile():
    print("compile complete")


def test():
    print("test complete")


def package():
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
