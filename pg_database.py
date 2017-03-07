# coding=utf-8

from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Table, Column, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = sqlalchemy.create_engine('postgresql://orunmila:neuralnet@198.199.104.56/orunmila')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Users(Base):
    """A base model to create users """

    __tablename__ = 'users'

    username = Column(String(50), primary_key=True)
    password = Column(String(50))
    email = Column(String(255))


class Clients():

    __tablename__ = 'clients'

    client_id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    surname = Column(String(255))
    email = Column(String(255))
    cellphone = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Projects():

    __tablename__ = 'projects'

    project_id = Column(Integer(), primary_key=True)
    project_code = Column(String(100))
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    latitude = Column(String(55))
    longitude = Column(String(55))
    tile = Column(String(55))
    crop = Column(String(100))
    analysis = Column(String(55))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Zora():

    __tablename__ = 'zora'
    analysis_id = Column(String(200))
    analysis_point = Column(String(200))


Base.metadata.create_all(engine)


""" App user functions """

def add_user(username, password, mail):
    cc_users = Users(username=username, password=password, mail=mail)
    session.add(cc_users)
    session.commit()


def delete_user(username):
    query = session.query(Users)
    query = query.filter(Users.cookie_name == username)
    dcc_user = query.one()
    session.delete(dcc_user)
    session.commit()


def modify_user():
    pass


def search_user_password(user):
    try:
        password = session.query(Users).filter(Users.password == user).first()
        return password
    except:
        return None
