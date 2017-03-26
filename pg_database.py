# coding=utf-8

from datetime import datetime
import sqlalchemy
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, Numeric, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = sqlalchemy.create_engine('postgresql://orunmila:neuralnet@198.199.104.56/orunmila', pool_recycle=1800)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Users(Base):
    """A base model to create users """

    __tablename__ = 'users'

    username = Column(String(50), primary_key=True)
    password = Column(String(50))
    email = Column(String(255))


class Clients(Base):

    __tablename__ = 'clients'

    client_id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255))
    surname = Column(String(255))
    email = Column(String(255))
    cellphone = Column(String(15))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Projects(Base):

    __tablename__ = 'projects'

    project_id = Column(Integer(), primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    project_code = Column(String(100))
    latitude = Column(String(55))
    longitude = Column(String(55))
    tile = Column(String(55))
    analysis = Column(String(55))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Zora(Base):

    __tablename__ = 'zora'
    analysis_id = Column(String(200), primary_key=True)
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
        info = session.query(Users).filter(Users.username == user).first()
        return info.password
    except:
        return None


def add_client(name, surname, email, cellphone):
    cc_client = Clients(name=name, surname=surname, email=email, cellphone=cellphone)
    session.add(cc_client)
    session.commit()


def search_client(email):
    try:
        info = session.query(Clients).filter(Clients.email == email).first()
        return info
    except:
        return None


def add_project(email, project_code, latitude, longitude, tile, analysis):
    info = search_client(email)
    cc_project = Projects(client_id=info.client_id, project_code=project_code, latitude=latitude, longitude=longitude,
                          tile=tile, analysis=analysis)
    session.add(cc_project)
    session.commit()
