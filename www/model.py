# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True, nullable=False)
	email = Column(String(100))
	username = Column(String(100))
	password = Column(String(100))
	is_admin = Column(Boolean)
	avatar_url = Column(String(200))
	created_at = Column(DateTime)

# class Blog(Base):
# 	pass

# class Comment(Base):
# 	pass


engine = create_engine('mysql+mysqlconnector://root:@localhost:3306/db_test')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def main():
	session = Session()
	user1 = User(username='pheynix', email='pheynixdu@gmail.com')
	user2 = User(username='skye', email='skye@hbo.com')
	session.add(user1)
	session.add(user2)
	session.commit()
	session.close()


if __name__ == '__main__':
	main()
	# pass