# database_setup.py
"""Python script for creating the database."""

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from config import get_database_uri

Base = declarative_base()

class User(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    email = Column(String(256), nullable=False)
    password_hash = Column(String(256), nullable=False)
    name = Column(String(256), nullable=True)
    login_date = Column(DateTime, nullable=False, default=func.now())

class Bot(Base):
    __tablename__ = 'bot'

    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey('account.id'))
    bot_image = Column(String(128), nullable=False, default='bot_default.png')
    bot_name = Column(String(256), nullable=False, default='ChatBot')
    bot_availability = Column(String(16), nullable=False, default='N')
    auto_add = Column(Boolean, nullable=False, default=False)
    bot_views = Column(Integer, nullable=False, default=0)
    modified_date = Column(DateTime, nullable=False, onupdate=func.now())
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'bot_name': self.bot_name,
            'bot_availability': self.bot_availability,
            'bot_views': self.bot_views,
            'modified_date': self.modified_date
        }

class Chatlog(Base):
    __tablename__ = 'chatlog'

    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey('account.id'))
    client_ip = Column(String(32), nullable=True)
    bot_log = Column(String(4096), nullable=True)
    created_date = Column(Date, nullable=False, default=func.now())
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'bot_id': self.bot_id,
            'client_ip': self.client_ip,
            'bot_log': self.bot_log,
            'created_date': self.created_date
        }

class Knowledge(Base):
    __tablename__ = 'knowledge'

    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey('account.id'))
    type = Column(String(16), nullable=False, default='Q')
    pattern = Column(String(512), nullable=False) 
    template = Column(String(1024), nullable=True)
    action = Column(String(256), nullable=True)
    created_date = Column(DateTime, nullable=False, default=func.now())
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'bot_id': self.bot_id,
            'type': self.type,
            'pattern': self.pattern,
            'template': self.template,
            'action': self.action,
            'created_date': self.created_date
        }

engine = create_engine(get_database_uri())
Base.metadata.create_all(engine)
