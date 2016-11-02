# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging; logging.basicConfig(level=logging.INFO)
import asyncio
from aiohttp import web

HOST = '127.0.0.1'
PORT = 8888

async def index(request):
	return web.Response(body=b'<h1>Hello!</h1>', content_type='text/html', charset='utf-8')

async def init(loop):
	app = web.Application(loop=loop)
	app.router.add_route('GET', '/', index)
	logging.info('server started at %s:%d' % (HOST, PORT))
	return await loop.create_server(app.make_handler(), HOST, PORT)

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()