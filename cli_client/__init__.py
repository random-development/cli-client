#!/usr/bin/env python
#pylint: disable=missing-docstring

import sys
import argparse

def get_args(args):
    parser = argparse.ArgumentParser(description="CLI for monitoring resources.")
    parser.add_argument(
        "-e",
        "--endpoint",
        required=True,
        help="Enpoint for gathering monitoring data.")
    parser.add_argument(
        "-u",
        "--username",
        required=True,
        help="Username for API Gateway authentication.")
    parser.add_argument(
        "-p",
        "--password",
        required=True,
        help="Password for API Gateway authentication.")
    return parser.parse_args(args)


def main():
    args = get_args(sys.argv[1:])
    print(
        "Hello cli-client with endpoint: {}, username: {}, pass: {}!".format(
            args.endpoint,
            args.username,
            args.password))
