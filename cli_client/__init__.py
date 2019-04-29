#!/usr/bin/env python
#pylint: disable=missing-docstring

import sys
import asyncio
import argparse
import logging
from cli_client import api_gateway, console
logging.basicConfig(level=logging.WARNING)

def get_args(args):
    parser = argparse.ArgumentParser(
        description="CLI for monitoring resources.")
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
    parser.add_argument(
        "-d",
        "--delay",
        type=int,
        default=2,
        help="Delay time (default 2 sec).")
    parser.add_argument(
        "-m",
        "--metrics",
        nargs="+",
        default=["cpu"],
        help="Metrics to show - space separated list. "
             "First element defines key for sorting to "
             "display top resources (default cpu).")
    return parser.parse_args(args)

def periodic(period):
    def scheduler(fcn):
        async def wrapper(*args, **kwargs):
            while True:
                asyncio.create_task(fcn(*args, **kwargs))
                await asyncio.sleep(period)
        return wrapper
    return scheduler

def main():
    args = get_args(sys.argv[1:])

    @periodic(args.delay)
    async def main_loop(token):
        data_to_print = await api_gateway.get_data(args.endpoint, token)
        await console.print_data(args.metrics, data_to_print)

    try:
        asyncio.run(console.print_data(args.metrics)) # plot empty dashboard
        asyncio.run(main_loop(
            api_gateway.get_token(args.username, args.password)))
    except KeyboardInterrupt:
        print("\n\nThank you for making this little program very happy.\n")
