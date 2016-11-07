from framework import get, post
from aiohttp import web
import model

@get('/')
async def index(request):
	session = model.Session()
	blogs = session.query(model.Blog).all()
	return {
		'__template__':'index.html',
		'blogs':blogs
	}


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

@get('/api/v1/users')
async def api_user(request):
	session = model.Session()
	users = session.query(model.User).all()
	for user in users:
		user.password = '******'
	# return {'users':users}
	return {
		'name':'skye',
		'friends':{
			'josh':{
				'name':'josh',
				'age': 10
			},
			'sansa':{
				'name': 'sansa', 
				'age':18
			}
		}, 
		'phone':None
	}