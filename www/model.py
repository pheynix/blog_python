# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, BigInteger, String, Text, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from time import time
from config import configs

Base = declarative_base()

# class StrMixIn(object):
# 	@declared_attr
# 	def __getattr__(self, attr):
# 		print('hhahahahahaha')
# 		if attr in dir(self):
# 			if isinstance(self.attr, bytearray):
# 				return self.attr.decode('utf-8')
# 			else:
# 				return self.attr
# 		else:
# 			raise AttributeError()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True, nullable=False)
	email = Column(String(100), nullable=False)
	username = Column(String(100), nullable=False)
	# Column('username', String(100), nullable=False)
	password = Column(String(100), nullable=False)
	is_admin = Column(Boolean, default=False)
	avatar_url = Column(String(200), default='/www/static/default_avatar.png')
	created_at = Column(BigInteger, default=time)

	blogs = relationship('Blog')

class Blog(Base):
	__tablename__ = 'blog'

	id = Column(Integer, primary_key=True, nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	title = Column(String(100), nullable=False)
	summary = Column(Text())
	content = Column(Text())
	created_at = Column(BigInteger, default=time)

	comments = relationship('Comment')


class Comment(Base):
	__tablename__ = 'comment'
	id = Column(Integer, primary_key=True, nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	blog_id = Column(Integer, ForeignKey('blog.id'))
	content = Column(Text(), nullable=False)
	created_at = Column(BigInteger, default=time)


db = configs['db']
url = 'mysql+mysqlconnector://%s:%s@%s:%s/%s' % (db['user'], db['password'], db['host'], db['port'], db['db'])
engine = create_engine(url, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def main():
	session = Session()
	user1 = User(username='joe', password='password1', email='joe@gmail.com')
	user2 = User(username='skye', password='password2', email='skye@hbo.com')
	session.add(user1)
	session.add(user2)
	session.commit()

	blog1 = Blog(user_id=1, title='论吃饭的重要性')
	blog2 = Blog(user_id=2, title='什么才是世界上最好的语言')
	session.add(blog1)
	session.add(blog2)
	session.commit()

	comment1 = Comment(user_id=2, blog_id=1, content='食屎啦你')
	comment2 = Comment(user_id=1, blog_id=2, content='php不服来辩')
	session.add(comment1)
	session.add(comment2)
	session.commit()

	session.close()


if __name__ == '__main__':
	main()
	# pass