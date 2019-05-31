#!/usr/bin/env python
#pylint: disable=missing-docstring

import io
import unittest
from unittest import mock
import cli_client.console as ccc


class TestConsole(unittest.TestCase):

    test_metric = 'hello my metric'
    test_empty_data = ""
    test_data = "this is header\nfirst line\nsecond line"
    test_real_data = {
        ('komp_zepsuty', 'hostName'): {'cpu': 50},
        ('komp_zepsuty', 'hostName2'): {'temp': 99, 'cpu': 99}}
    test_real_metrics = ['cpu', 'temp', 'elo']

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_title(self, sys_stdout_mock):
        ccc.print_title(self.test_metric, 'test_time')
        self.assertTrue(self.test_metric in sys_stdout_mock.getvalue())

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_table_without_data(self, sys_stdout_mock):
        table_mock = mock.MagicMock()
        table_mock.get_string.return_value = self.test_empty_data
        ccc.print_table(table_mock)
        self.assertTrue("awaiting for data" in sys_stdout_mock.getvalue())

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_table_with_data_all_lines(self, sys_stdout_mock):
        table_mock = mock.MagicMock()
        table_mock.get_string.return_value = self.test_data
        ccc.print_table(table_mock)
        for line in self.test_data.split('\n'):
            with self.subTest(line=line):
                self.assertTrue(line in sys_stdout_mock.getvalue())

    def test_create_table_with_data(self):
        table = ccc.create_table_with_data(
            self.test_real_metrics,
            self.test_real_data)
        self.assertEqual(len(table._rows), 2) #pylint: disable=protected-access
