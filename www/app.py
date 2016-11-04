# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging; logging.basicConfig(level=logging.INFO)
import asyncio
from aiohttp import web
from framework import add_routes, add_static
from datetime import datetime

HOST = '127.0.0.1'
PORT = 8888


# http://aiohttp.readthedocs.io/en/stable/web.html#aiohttp-web-middlewares
async def logging_factory(app, handler):
	async def logger(request):
		logging.info('%s %s %s' % (str(datetime.now()), request.method, request.path))
		return await handler(request)
	return logger


async def init(loop):
	app = web.Application(loop=loop, middlewares=[logging_factory])
	add_routes(app, 'handlers')
	add_static(app)
	logging.info('server started at %s:%d' % (HOST, PORT))
	return await loop.create_server(app.make_handler(), HOST, PORT)

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()