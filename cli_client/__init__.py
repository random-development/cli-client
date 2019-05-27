#!/usr/bin/env python
#pylint: disable=missing-docstring

import sys
import time
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
    async def main_print_loop(data_to_print, metrics):
        await console.print_data(metrics, data_to_print)

    async def main_download_loop(data_to_update, token):
        while True:
            print("begin")
            data_to_update.data = await api_gateway.get_data(args.endpoint, token)
            data_to_update.time = time.ctime()

    async def main_loop(username, password, metrics):
        async_data = type('', (), {})()
        async_data.data = {}
        async_data.time = time.strftime('%a %b %d %H:%M:%S %Y', time.gmtime(0))
        await asyncio.gather(
            main_download_loop(
                async_data,
                api_gateway.get_token(username, password)),
            main_print_loop(async_data, metrics))

    try:
        asyncio.run(main_loop(args.username, args.password, args.metrics))
    except KeyboardInterrupt:
        print("\n\nThank you for making this little program very happy.\n")
