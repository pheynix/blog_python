# !/usr/bin/env python3
# -*- coding: utf-8 -*-


import functools
import inspect
import asyncio
import logging
from importlib import import_module


def get(path):
	def decorator(fn):
		@functools.wraps(fn)
		def wrapper(*args, **kw):
			return fn(*args, **kw)
		wrapper.__path__ = path
		wrapper.__method__ = 'GET'
		return wrapper
	return decorator


def post(path):
	def decorator(fn):
		@functools.wraps(fn)
		def wrapper(*args, **kw):
			return fn(args, kw)
		wrapper.__path__ = path
		wrapper.__method__ = 'POST'
		return wrapper
	return decorator


def add_route(app, fn):
	method = getattr(fn, '__method__', None)
	path = getattr(fn, '__path__', None)

	if not method or not path:
		raise ValueError('未使用@get或者@post: %s' % fn.__name__)
	elif not inspect.iscoroutinefunction(fn) or not inspect.isnogeneratorfunction(fn):
		fn = asyncio.coroutine(fn)

	logging.info('adding route: %s %s to %s' % (method, path, fn.__name__))
	app.router.add_route(method, path, fn)


def add_routes(app, module_name):
	mod = import_module_(module_name)
	for attr in dir(mod):
		if attr.startswith('_'):
			continue
		else:
			fn = getattr(mod, attr)
			if callable(fn):
				method = getattr(fn, '__method__', None)
				path = getattr(fn, '__path__', None)
				if method and path:
					add_route(app, fn)



def import_module_(module_name):
	n = module_name.rfind('.')
	if n == (-1):
		return import_module(module_name)
	else:
		raise ValueError('暂时只支持同包的模块导入')

def main():
	class Router(object):
		def add_route(self, method, path, fn):
			print(method, path, fn)

	class App(object):
		pass

	app = App()
	app.router = Router()
	def fn():
		pass
	fn.__method__ = 'GET'
	fn.__path__ = '/home'
	# add_route(app, fn)

	add_routes(app, 'handlers')



if __name__ == '__main__':
	main()