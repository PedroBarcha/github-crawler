import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

Base = declarative_base()


# declare tables objects Repository e lista de url
class Repository(Base):
    __tablename__ = 'repositorios'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100))
    owner = Column('owner', String(50))
    license = Column('license', String(100))
    forkCount = Column('forkCount', Integer)
    stargazerCount = Column('stargazerCount', Integer)
    watchersCount = Column('Watchers', Integer)
    openIssues = Column('Issues', Integer)
    updatedAt = Column('update', DateTime)
    pushedAt = Column('push', DateTime)
    commits = Column('commits', Integer)
    collaborators = Column('collaborators', Integer)


class UrlList(Base):
    __tablename__ = "ListaURL"

    id = Column('id', Integer, primary_key=True)
    repo_id = Column('repo_id', Integer, ForeignKey('repositorios.id'))
    url = Column('URL', String(250))
    visitado = Column('Visitado', Boolean, default=False, nullable=False)
    erro = Column('erro', Boolean, nullable=True, default=False)


# start db connection
# TODO:change engine call to accept others relational databases
# TODO:fix env variables
engine = db.create_engine(os.environ.get('DB_CLIENT') + '://' + os.environ.get('DB_USER') + ':' + os.environ.get(
    'DB_PASSWORD') + '@' + os.environ.get('DB_HOST') + '/' + os.environ.get('DB_NAME'))
connection = engine.connect()
metadata = db.MetaData()
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()
