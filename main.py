#!/usr/bin/env python3

import sys
if sys.version_info < (3, 7):
    sys.stderr.write("Sorry, this program requires Python 3.7\n")
    sys.exit(1)

import cli_client #pylint: disable=wrong-import-position

if __name__ == '__main__':
    cli_client.main()
