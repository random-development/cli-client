#!/usr/bin/env python
#pylint: disable=missing-docstring

import os
import time
import logging
import prettytable
from huepy import bg #pylint: disable=no-name-in-module

LOGGER = logging.getLogger('console')

CURSOR_0_0 = '\033[H'

def clear_screen(ver):
    if ver == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def print_title(metric, gateway_time):
    print(f"{CURSOR_0_0}{time.ctime()} (API Gateway response from {gateway_time})"
          f" - Top for '{metric}' metric")

def print_table(table):
    full_table_string = table.get_string(start=0, end=10).split(os.linesep)
    if len(full_table_string) == 1:
        print("(awaiting for data)")
    else:
        print(os.linesep.join([
            bg(full_table_string[0]),
            *full_table_string[1:]]))

def create_empty_table(metrics):
    table = prettytable.PrettyTable()
    table.field_names = ["monitor", "resource", *metrics]
    table.border = False
    table.header = True
    table.float_format = ".1"
    table.header_style = 'upper'
    table.max_table_width = 80
    table.align = "r"
    table.sortby = metrics[0]
    table.reversesort = True
    return table

def create_table_with_data(metrics_labels, data):
    table = create_empty_table(metrics_labels)
    for resource, metrics in data.items():
        table.add_row([
            resource[0],
            resource[1],
            *[metrics.get(l, -1.0) for l in metrics_labels]])
    return table

async def print_data(metrics, data):
    table = create_empty_table(metrics)
    if data.data:
        LOGGER.debug("Fullfil table with data: %s", data.data)
        table = create_table_with_data(metrics, data.data)
    clear_screen(os.name)
    print_title(metrics[0], data.time)
    print_table(table)
