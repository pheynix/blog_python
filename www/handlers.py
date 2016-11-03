from framework import get, post
from aiohttp import web

@get('/')
async def index(request):
	return web.Response(body=b'<h1>Hello!</h1>', content_type='text/html', charset='utf-8')

@get('/login')
async def login(request):
	return web.Response(body=b'<h1>Login!</h1>', content_type='text/html', charset='utf-8')


