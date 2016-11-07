# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging; logging.basicConfig(level=logging.INFO)
import asyncio
import json
import os
import time
from aiohttp import web
from framework import add_routes, add_static
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


HOST = '127.0.0.1'
PORT = 8888


# 打印请求
# http://aiohttp.readthedocs.io/en/stable/web.html#aiohttp-web-middlewares
async def logging_factory(app, handler):
	async def logger(request):
		logging.info('%s %s %s' % (str(datetime.now()), request.method, request.path))
		return await handler(request)
	return logger


# 格式化POST请求的body
async def request_factory(app, handler):
	async def parse_data(request):
		if request.method == 'POST':
			if request.content_type.startswith('application/json'):
				request.__data__ = request.json()
				logging.info('post json %s' % str(request.__data__))
			elif request.content_type.startswith('application/x-www-form-urlencoded'):
				request.__data__ = request.post()
				logging.info('post form %s' % str(request.__data__))
		return await handler(request)
	return parse_data


# 格式化响应结果 web.StreamResponse bytes str dict int tuple default
async def response_factory(app, handler):
	async def assemble_response(request):
		result = await handler(request)
		if isinstance(result, web.StreamResponse):
			logging.info('response web.StreamResponse:')
			return result
		elif isinstance(result, bytes):
			resp = web.Response(body=result)
			resp.content_type = 'application/octet-stream'
			logging.info('response bytes: %s' % result.decode('utf-8'))
			return resp
		elif isinstance(result, str):
			logging.info('response str: %s' % result)
			if result.startswith('redirect:'):
				return web.HTTPFound(r[9:])
			else:
				resp = web.Response(body=result.encode('utf-8'))
				resp.content_type = 'text/html;charset=utf-8'
				return resp
		elif isinstance(result, dict):
			template = result.get('__template__')
			if template is None:
				def fn(o):
					if hasattr(o, '__dict__'):
						if isinstance(result, bytes):
							return result.decode('utf-8').__dict__
						else:
							return result.__dict__

				body = json.dumps(result, ensure_ascii=False, default=lambda o: o.__dict__)
				resp = web.Response(body=body.encode('utf-8'))
				resp.content_type = 'application/json;charset=utf-8'
				logging.info('response json: %s' % body)
				return resp
			else:
				body = app['__templating__'].get_template(template).render(**result)
				resp = web.Response(body=body.encode('utf-8'))
				resp.content_type = 'text/html;charset=utf-8'
				logging.info('response html:')
				return resp
		elif isinstance(result, int) and result >= 100 and result <= 600:
			logging.info('response status: %s' % result)
			return web.Response(result)
		elif isinstance(result, tuple) and len(result) == 2:
			status, body = result
			logging.info('response tuple: %s' % result)
			return web.Response(status, str(body))
		else:
			resp = web.Response(body=str(r).encode('utf-8'))
			resp.content_type = 'text/plain;charset=utf-8'
			return resp;
	return assemble_response;


def datetime_filter(t):
	delta = int(time.time() - t)
	if delta < 60:
		return u'1分钟前'
	if delta < 3600:
		return u'%s分钟前' % (delta // 60)
	if delta < 86400:
		return u'%s小时前' % (delta // 3600)
	if delta < 604800:
		return u'%s天前' % (delta // 86400)
	dt = datetime.fromtimestamp(t)
	return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

def init_jinja(app, **kw):
	options = dict(
		autoescape = kw.get('autoescape', True),
		block_start_string = kw.get('block_start_string', '{%'),
		block_end_string = kw.get('block_end_string', '%}'),
		variable_start_string = kw.get('variable_start_string', '{{'),
		variable_end_string = kw.get('variable_end_string', '}}'),
		auto_reload = kw.get('auto_reload', True)
	)
	path = kw.get('path', None)
	if not path:
		template_dir = os.path.dirname(os.path.abspath(__file__))
		path = os.path.join(template_dir, 'templates')
	logging.info('adding templates: %s' % path)
	env = Environment(loader=FileSystemLoader(path), **options)
	filters = kw.get('filters', None)
	if filters is not None:
		for name, f in filters.items():
			env.filters[name] = f
	app['__templating__'] = env



async def init(loop):
	app = web.Application(loop=loop, middlewares=[logging_factory ,request_factory, response_factory])
	add_routes(app, 'handlers')
	add_static(app)
	init_jinja(app, filters=dict(datetime=datetime_filter))
	logging.info('server started at %s:%d' % (HOST, PORT))
	return await loop.create_server(app.make_handler(), HOST, PORT)

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()