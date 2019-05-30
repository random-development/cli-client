#!/usr/bin/env python
#pylint: disable=missing-docstring

import pytest
import unittest
from unittest import mock
import cli_client.api_gateway as ag

class TestApiGateway(unittest.TestCase):

    def test_get_cli_client_creds(self):
        mocked_environment = {
            "CLI_CLIENT_USER": "aaa",
            "CLI_CLIENT_PASSWORD": "bbb"
        }
        with mock.patch.dict("cli_client.api_gateway.os.environ", mocked_environment):
            self.assertEqual(
                ag.get_cli_client_creds(),
                tuple(mocked_environment.values()))

    def test_get_cli_client_creds_incomplete_environment(self):
        mocked_environment = {
            "CLI_CLIENT_USER": "aaa"
        }
        with mock.patch.dict("cli_client.api_gateway.os.environ", mocked_environment) and \
            self.assertRaisesRegex(SystemExit, "2"):
                ag.get_cli_client_creds()
