#!/usr/bin/env python
#pylint: disable=missing-docstring

import os
import sys
import logging
from urllib import parse

import aiohttp

LOGGER = logging.getLogger('api_gateway')

def get_cli_client_creds():
    user = os.environ.get("CLI_CLIENT_USER")
    password = os.environ.get("CLI_CLIENT_PASSWORD")
    if user and password:
        return user, password
    sys.stderr.write(
        "Error: CLI Client requires defining "
        "'CLI_CLIENT_USER' and 'CLI_CLIENT_PASSWORD' variables.\n")
    sys.exit(2)

async def send_request(endpoint, method):
    async with aiohttp.ClientSession() as session:
        async with method(session, endpoint) as response:
            try:
                return await response.json(), response.status
            except aiohttp.client_exceptions.ContentTypeError:
                return await response.text(), response.status

async def get_token(auth_endpoint, username, password):
    LOGGER.debug("Getting token for user %s", username)
    client_user, client_pass = get_cli_client_creds()
    raw_auth_endpoint = parse.urlparse(auth_endpoint)
    endpoint = f"{raw_auth_endpoint.scheme}://{client_user}:{client_pass}@" \
        f"{raw_auth_endpoint.netloc}/oauth/token?grant_type=password" \
        f"&username={username}&password={password}"
    resp, _ = check_status(*(await send_request(endpoint, aiohttp.ClientSession.post)))
    return resp['access_token']

async def get_data_from_endpoint(endpoint, token):
    return await send_request(endpoint + f"?access_token={token}", aiohttp.ClientSession.get)

def check_status(response, status):
    if status != 200:
        try:
            sys.stderr.write(
                f"Error {status}: ({response['error']}): {response['error_description']}\n")
        except TypeError:
            sys.stderr.write(f"Error {status}: {response}\n")
        sys.exit(3)
    return response, status

async def get_data(data_endpoint, auth_endpoint, user_username, user_password, token=None):
    metrics_endpoint = parse.urljoin(data_endpoint, "metrics")
    LOGGER.info("Gathering data from endpoint '%s'", metrics_endpoint)
    #FIXME: #40 Gather all records in form:
    # [[MONITOR, RESOURCE, {metric1: value1, metric2: value2}]] and return them
    response, status = await get_data_from_endpoint(metrics_endpoint, token)
    if status == 401: # need to generate new token
        token = await get_token(auth_endpoint, user_username, user_password)
        return check_status(*(await get_data_from_endpoint(metrics_endpoint, token)))[0], token
    return response, token
