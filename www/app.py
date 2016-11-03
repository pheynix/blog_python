# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging; logging.basicConfig(level=logging.INFO)
import asyncio
from aiohttp import web
from framework import add_routes

HOST = '127.0.0.1'
PORT = 8888


async def init(loop):
	app = web.Application(loop=loop)
	add_routes(app, 'handlers')
	logging.info('server started at %s:%d' % (HOST, PORT))
	return await loop.create_server(app.make_handler(), HOST, PORT)

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()