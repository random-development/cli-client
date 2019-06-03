#!/usr/bin/env python
#pylint: disable=missing-docstring

import unittest
from unittest import mock

import pytest
from asynctest import CoroutineMock
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

    def test_check_status_ok(self):
        test_response = 'test'
        test_status = 200
        self.assertEqual(len(ag.check_status(test_response, test_status)), 2)

    def test_check_status_nok(self):
        test_response = 'test'
        test_status = 500
        with self.assertRaisesRegex(SystemExit, "3"):
            ag.check_status(test_response, test_status)

class TestGatherRecords(unittest.TestCase):

    test_data_from_endpoint = [
        {
            "name": "hostName",
            "resourceName": "komp_zepsuty",
            "type": "cpu",
            "lastValue": 50,
            "time": 1554663619,
            "timeData": [1554663615, 1554663616, 1554663617, 1554663618, 1554663619],
            "valueData": [213, 214, 215, 264, 214]
        },
        {
            "name": "hostName2",
            "resourceName": "komp_zepsuty",
            "type": "temp",
            "lastValue": 99,
            "time": 1554643619,
            "timeData": [1554643615, 1554643616, 1554643617, 1554643618, 1554643619],
            "valueData": [78, 88, 97, 98, 99]
        },
        {
            "name": "hostName2",
            "resourceName": "komp_zepsuty",
            "type": "cpu",
            "lastValue": 99,
            "time": 1554643619,
            "timeData": [1554643615, 1554643616, 1554643617, 1554643618, 1554643619],
            "valueData": [78, 88, 97, 98, 99]
        }
    ]

    def test_same_monitors(self):
        records = ag.gather_records(self.test_data_from_endpoint)
        self.assertEqual(len(records), 2)

    def test_metrics(self):
        records = ag.gather_records(self.test_data_from_endpoint)
        for metric, test_case in {'cpu': 2, 'temp': 1, 'elo': 0}.items():
            with self.subTest(metric=metric):
                self.assertEqual(
                    sum(1 for resource in records.values() if resource.get(metric) is not None),
                    test_case)

@pytest.mark.asyncio
async def test_get_token():
    endpoint = 'http://localhost:7000'
    username = 'enduser'
    password = 'password'
    cli_username = 'automatic-client'
    cli_password = 'noonewilleverguess3'
    with mock.patch('cli_client.api_gateway.send_request', new=CoroutineMock()) \
            as send_request_mock:
        with mock.patch('cli_client.api_gateway.get_cli_client_creds') as creds_mock:
            creds_mock.return_value = (cli_username, cli_password)
            with mock.patch('cli_client.api_gateway.check_status') as check_status_mock:
                check_status_mock.return_value = ({'access_token': 'test'}, 'tmp')
                await ag.get_token(endpoint, username, password)
                send_request_mock.assert_called_once_with(
                    f'http://{cli_username}:{cli_password}@localhost:7000/oauth/token'
                    f'?grant_type=password&username={username}&password={password}',
                    ag.aiohttp.ClientSession.post)

@pytest.mark.asyncio
async def test_get_data_from_endpoint():
    endpoint = 'http://awesome.endpoint:7000'
    token = 'eloelo320'
    with mock.patch('cli_client.api_gateway.send_request', new=CoroutineMock()) \
            as send_request_mock:
        await ag.get_data_from_endpoint(endpoint, token)
        send_request_mock.assert_called_once_with(
            f'{endpoint}?access_token={token}', ag.aiohttp.ClientSession.get)

@pytest.mark.asyncio
async def test_get_data_without_token():
    test_endpoint = 'http://awesome.endpoint:7000/'
    test_username = 'user'
    test_password = 'pass'
    with mock.patch('cli_client.api_gateway.get_data_from_endpoint', new=CoroutineMock()) \
            as data_mock:
        data_mock.return_value = ('', 401)
        with mock.patch('cli_client.api_gateway.get_token', new=CoroutineMock()) as get_token_mock:
            get_token_mock.return_value = "eloelo320"
            with mock.patch('cli_client.api_gateway.check_status'):
                await ag.get_data(test_endpoint, test_endpoint, test_username, test_password)
                get_token_mock.assert_called_once_with(test_endpoint, test_username, test_password)

@pytest.mark.asyncio
async def test_get_data_with_token():
    test_endpoint = 'http://awesome.endpoint:7000/'
    test_username = 'user'
    test_password = 'pass'
    with mock.patch('cli_client.api_gateway.get_data_from_endpoint', new=CoroutineMock()) \
            as data_mock:
        data_mock.return_value = ('', 200)
        with mock.patch('cli_client.api_gateway.get_token', new=CoroutineMock()) as get_token_mock:
            with mock.patch('cli_client.api_gateway.check_status'):
                await ag.get_data(test_endpoint, test_endpoint, test_username, test_password)
                get_token_mock.assert_not_called()
