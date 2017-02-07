# dummyrecords.py
"""Python script for inserting dummyrecordsin database."""

import random
import string
import codecs
import hashlib
import hmac

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Chatlog, Knowledge, Bot, User
from config import get_database_uri

# helper function definations

def make_salt(length=5):
    """Creates random string of length same as passed parameter."""

    salt = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in xrange(length))
    return salt


def make_password_hash(email, password, salt=None):
    """Creates hash using passed parameters."""

    if not salt:
        salt = make_salt()
    hash_val = hashlib.sha256(email + password + salt).hexdigest()

    return '%s,%s' % (salt, hash_val)

engine = create_engine(get_database_uri())
engine.connect().connection.text_factory = str
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
pw_hash = make_password_hash('kaushal.meena1996@gmail.com', '123')
user1 = User(id=1,
             name='kaushal',
             password_hash=pw_hash,
             email='kaushal.meena1996@gmail.com')
session.add(user1)
session.commit()

bot1 = Bot(id=1,
           bot_id=user1.id,
           bot_image='bot_default.png',
           bot_name='ChatBot',
           bot_availability='N',
           auto_add=False,
           bot_views=0,
           modified_date=func.now(),
           user=user1)
session.add(bot1)
session.commit()

print "added records..."
