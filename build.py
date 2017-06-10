#!/usr/bin/env python
import argparse


def hello():
    print("setup")
    print("compile")
    print("test")
    print("package")

parser = argparse.ArgumentParser(description='Build it')
parser.add_argument('--list_steps', action='store_true')

args = parser.parse_args()

if args.list_steps:
    hello()
