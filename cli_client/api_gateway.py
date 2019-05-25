#!/usr/bin/env python
#pylint: disable=missing-docstring

import logging
from urllib import parse

import aiohttp

LOGGER = logging.getLogger('api_gateway')


def get_token(username, password): #pylint: disable=unused-argument
    #FIXME: #49 Get token from auth microservice using user&pass
    return 'eloelo320'

async def get_data_from_endpoint(endpoint, _):
    #FIXME: #49 Implement using token during http connection
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as response:
            return await response.json()

async def get_data(endpoint, token):
    metrics_endpoint = parse.urljoin(endpoint, "metrics")
    LOGGER.info("Gathering data from endpoint '%s'", metrics_endpoint)
    #FIXME: #40 Gather all records in form:
    # [[MONITOR, RESOURCE, {metric1: value1, metric2: value2}]] and return them
    return await get_data_from_endpoint(metrics_endpoint, token)
