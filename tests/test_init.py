#!/usr/bin/env python
#pylint: disable=missing-docstring

import unittest
from unittest import mock
import cli_client

class TestInit(unittest.TestCase):
    test_endpoint = "test endpoint name"
    test_username = "test username"
    test_password = "test password"

    def test_get_args_proper_args(self):
        parser = cli_client.get_args([
            "-e",
            self.test_endpoint,
            "-a",
            self.test_endpoint,
            "-u",
            self.test_username,
            "-p",
            self.test_password])
        self.assertTrue(parser.data_endpoint, self.test_endpoint)

    @mock.patch("sys.exit")
    def test_get_args_incomplete_args(self, sys_exit_mock):
        _ = cli_client.get_args(["-e", self.test_endpoint])
        sys_exit_mock.assert_called_once_with(2)
