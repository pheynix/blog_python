from framework import get, post
from aiohttp import web
import model

@get('/')
async def index(request):
	return web.Response(body=b'<h1>Hello!</h1>', content_type='text/html', charset='utf-8')


@post('/login')
async def login(request):
	return dict(name='doge', age=10, is_admin=False)


@get('/users')
async def all_user(request):
	session = model.Session()
	users = session.query(model.User).all()
	return {
		'__template__': 'users.html',
		'users':users
	}