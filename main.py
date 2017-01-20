# server.py
"""Python script for server implementation."""

# python imports
from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from socket import gethostname, gethostbyname

from sqlalchemy import create_engine, asc, func, desc
from sqlalchemy.orm import sessionmaker
from database.database_setup import Base, Chatlog, Knowledge, Bot, User
from database.config import get_database_uri

from flask import session as login_session
from functools import wraps

from math import ceil

from secret.secret import get_secret

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import smtplib
from flask import make_response
import requests
import random
import string
import os

from helper.helper import (make_password_hash,
                           validate_password,
                           valid_email,
                           valid_password,
                           read_secure_cookie,
                           make_secure_val,
                           check_secure_val,
                           show_pagination00,
                           show_pagination01)

app = Flask(__name__)

APPLICATION_NAME = "MakeMyBot"

port = int(os.environ.get('PORT', 33507))

# Connect to Database and create database session
engine = create_engine(get_database_uri())
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# LOG Conversation


def log_conversation(bot_id, message_type, message, response):
    botInfo = session.query(Bot).filter_by(id=bot_id).one_or_none()

    client_ip = gethostbyname(gethostname())
    bot_name = botInfo.bot_name

    if message_type == 'Q':
        line = "\nUSER\t: %s\n%s : %s" % (message, bot_name, response)
    if message_type == 'G':
        line = "\n%s\t: %s" % (bot_name, response)
    if message_type == 'E':
        line = "\n----------------------------------"

    browse_data = session.query(Chatlog).\
        filter_by(bot_id=bot_id).\
        filter_by(created_date=func.current_date()).\
        filter_by(client_ip=client_ip).\
        first()

    if browse_data:
        browse_data.bot_log += line
        session.add(browse_data)
        session.commit()

    else:
        newChatLog = Chatlog(bot_id=bot_id,
                             client_ip=client_ip,
                             bot_log=line,
                             created_date=func.current_date())

        session.add(newChatLog)
        session.commit()


# Decorated functions


def cookie_check(f):
    """Creates login_session after verifying cookie."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'name' not in login_session:
            user_id = read_secure_cookie("user_id")
            if user_id:
                user = getUserInfo(user_id)
                if user:
                    login_session['provider'] = 'app'
                    login_session['user_id'] = user.id
                    login_session['name'] = user.name
                    login_session['email'] = user.email

        return f(*args, **kwargs)
    return decorated_function


# Login page


@cookie_check
@app.route('/login', methods=['GET', 'POST'])
def showLogin():
    """"Handler for LOGIN page which allows users to login."""

    if 'user_id' in login_session:
        flash("you have alredy logged in.")
        return redirect(url_for('showHome'))
    else:
        if request.method == 'POST':
            email = request.form["e-mail"]
            password = request.form["password"]

            login_err = False

            if(len(email) < 3):
                flash("e-mail must have altleast 3 characters.")
                login_err = True

            elif not valid_email(email):
                flash("please enter valid e-mail.")
                login_err = True

            if(len(password) < 3):
                flash("password must have altleast 3 characters.")
                login_err = True

            elif not valid_password(password):
                flash("please enter valid password.")
                login_err = True

            if login_err:
                return render_template("login.html",
                                       menuTitle='Login',
                                       menuId='#menuLogin',
                                       menuColor='w3-col-purple',
                                       buttonColor='w3-button-col-purple',
                                       textColor='w3-text-col-purple',
                                       colorHex='#8E44AD',
                                       email=email,
                                       password=password)

            if loginUser(email, password):
                flash("login successful, welcome " +
                      login_session['name'] + ".")
                cookie_val = make_secure_val(str(login_session['user_id']))
                response = make_response(redirect(url_for('showHome')))
                response.set_cookie('user_id', cookie_val)
                return response
            else:
                flash("invalid name or password.")
                return render_template("login.html",
                                       menuTitle='Login',
                                       menuId='#menuLogin',
                                       menuColor='w3-col-purple',
                                       buttonColor='w3-button-col-purple',
                                       textColor='w3-text-col-purple',
                                       colorHex='#8E44AD',
                                       email=email,
                                       password=password)

        else:
            return render_template('login.html',
                                   menuTitle='Login',
                                   menuId='#menuLogin',
                                   menuColor='w3-col-purple',
                                   buttonColor='w3-button-col-purple',
                                   textColor='w3-text-col-purple',
                                   colorHex='#8E44AD')

# Register page


@cookie_check
@app.route('/register', methods=['GET', 'POST'])
def showRegister():
    """Handler for REGISTER page which allows users to register."""

    if 'user_id' in login_session:
        flash("you have alredy registered.")
        return redirect(url_for('showHome'))
    else:
        if request.method == 'POST':
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            confirm = request.form["confirm"]

            register_err = False

            if(len(email) < 3):
                flash("e-mail must have altleast 3 characters.")
                register_err = True

            elif not valid_email(email):
                flash("please enter valid e-mail.")
                register_err = True

            if(len(password) < 3):
                flash("password must have altleast 3 characters.")
                register_err = True

            elif not valid_password(password):
                flash("please enter valid password.")
                register_err = True

            if not password == confirm:
                flash("password and confirm don't match.")
                register_err = True

            if register_err:
                return render_template("register.html",
                                       menuTitle='Register',
                                       menuId='#menuRegister',
                                       menuColor='w3-col-purple',
                                       buttonColor='w3-button-col-purple',
                                       textColor='w3-text-col-purple',
                                       colorHex='#8E44AD',
                                       name=name,
                                       password=password,
                                       confirm=confirm,
                                       email=email)

            if registerUser(email, password, name):
                flash("registration successful, welcome " + name + ".")
                cookie_val = make_secure_val(str(login_session['user_id']))
                response = make_response(redirect(url_for('showHome')))
                response.set_cookie('user_id', cookie_val)
                return response
            else:
                flash("specified email alredy exists.")
                return render_template("register.html",
                                       menuTitle='Register',
                                       menuId='#menuRegister',
                                       menuColor='w3-col-purple',
                                       buttonColor='w3-button-col-purple',
                                       textColor='w3-text-col-purple',
                                       colorHex='#8E44AD',
                                       name=name,
                                       password=password,
                                       confirm=confirm,
                                       email=email)

        else:
            return render_template('register.html',
                                   menuTitle='Register',
                                   menuId='#menuRegister',
                                   menuColor='w3-col-purple',
                                   buttonColor='w3-button-col-purple',
                                   textColor='w3-text-col-purple',
                                   colorHex='#8E44AD')

# Setting pages


@cookie_check
@app.route('/user/setting/00', methods=['GET', 'POST'])
def showSetting00():
    """Renders SETTING page if user has logged in otherwise renders
       LOGIN page."""

    if 'user_id' in login_session:
        if request.method == 'POST':
            editUser = session.query(User).filter_by(
                id=login_session['user_id']).one_or_none()
            editBot = session.query(Bot).filter_by(
                bot_id=login_session['user_id']).one_or_none()

            bot_container = request.form["bot_container"]
            bot_name = request.form["bot_name"]
            bot_availability = request.form["bot_availability"]
            bot_add = request.form["bot_add"]
            profile_name = request.form["profile_name"]

            edit_err = False

            if editUser:
                if not profile_name:
                    flash("profile name can't be empty.")
                    edit_err = True

                if not bot_name:
                    flash("bot name can't be empty.")
                    edit_err = True

                if edit_err:
                    return render_template("setting.html",
                                           menuTitle='Setting',
                                           menuId='#menuSetting',
                                           menuColor='w3-col-darkgreen',
                                           buttonColor='w3-button-col-darkgreen',
                                           textColor='w3-text-col-darkgreen',
                                           colorHex='#16A085',
                                           profile_name=profile_name,
                                           bot_name=bot_name,
                                           botInfo=editBot)

                editUser.name = profile_name
                editBot.bot_name = bot_names
                editBot.bot_image = bot_container
                editBot.bot_availability = bot_availability
                editBot.bot_add = bot_add

                session.add(editUser)
                session.add(editBot)
                session.commit()
                flash("settings successfully updated.")
                return redirect(url_for('showSetting00'))
            else:
                flash("user not found in database.")
                return redirect(url_for('showHome'))

        else:
            botInfo = session.query(Bot).filter_by(
                bot_id=login_session['user_id']).one_or_none()
            return render_template('setting00.html',
                                   menuTitle='Setting',
                                   menuId='#menuSetting',
                                   menuColor='w3-col-darkgreen',
                                   buttonColor='w3-button-col-darkgreen',
                                   textColor='w3-text-col-darkgreen',
                                   colorHex='#16A085',
                                   profile_name=login_session['name'],
                                   bot_name=botInfo.bot_name,
                                   botInfo=botInfo)
    else:
        flash("you must be logged in first.")
        return redirect(url_for('showLogin'))


@cookie_check
@app.route('/user/setting/01', methods=['GET', 'POST'])
def showSetting01():
    """Renders SETTING-(CHANGEPASSWORD) page if user has logged in otherwise renders
       LOGIN page."""

    if 'user_id' in login_session:
        if request.method == 'POST':
            editUser = session.query(User).filter_by(
                id=login_session['user_id']).one_or_none()

            password = request.form["password"]
            confirm = request.form["confirm"]

            edit_err = False

            if editUser:
                if(len(password) < 3):
                    flash("password must have altleast 3 characters.")
                    edit_err = True

                elif not valid_password(password):
                    flash("please enter valid password.")
                    edit_err = True

                if not password == confirm:
                    flash("password and confirm don't match.")
                    edit_err = True

                if edit_err:
                    return render_template("setting01.html",
                                           menuTitle='Setting',
                                           menuId='#menuSetting',
                                           menuColor='w3-col-darkgreen',
                                           buttonColor='w3-button-col-darkgreen',
                                           textColor='w3-text-col-darkgreen',
                                           colorHex='#16A085')

                editUser.password_hash = make_password_hash(
                    login_session['email'], password)

                session.add(editUser)
                session.commit()
                flash("settings successfully updated.")
                return redirect(url_for('showSetting00'))
            else:
                flash("user not found in database.")
                return redirect(url_for('showHome'))

        else:
            return render_template("setting01.html",
                                   menuTitle='Setting',
                                   menuId='#menuSetting',
                                   menuColor='w3-col-darkgreen',
                                   buttonColor='w3-button-col-darkgreen',
                                   textColor='w3-text-col-darkgreen',
                                   colorHex='#16A085')
    else:
        flash("you must be logged in first.")
        return redirect(url_for('showLogin'))


@cookie_check
@app.route('/user/setting/02', methods=['GET', 'POST'])
def showSetting02():
    """Renders SETTING-(CHANGEPASSWORD) page if user has logged in otherwise renders
       LOGIN page."""

    if 'user_id' in login_session:
        if request.method == 'POST':
            editUser = session.query(User).filter_by(
                id=login_session['user_id']).one_or_none()

            if editUser:
                session.delete(editUser)
                session.commit()
                flash("account successfully deleted.")
                return redirect(url_for('showSetting00'))
            else:
                flash("user not found in database.")
                return redirect(url_for('showHome'))

        else:
            return render_template("setting02.html",
                                   menuTitle='Setting',
                                   menuId='#menuSetting',
                                   menuColor='w3-col-darkgreen',
                                   buttonColor='w3-button-col-darkgreen',
                                   textColor='w3-text-col-darkgreen',
                                   colorHex='#16A085')
    else:
        flash("you must be logged in first.")
        return redirect(url_for('showLogin'))


# User Helper Functions


def loginUser(email, password):
    """Validates user login's form information for errors and accordingly
       redirects the page."""

    users = session.query(User).filter_by(email=email).all()
    for user in users:
        if validate_password(email, password, user.password_hash):
            login_session['provider'] = 'app'
            login_session['user_id'] = user.id
            login_session['name'] = user.name
            login_session['email'] = user.email
            return True
    return False


def registerUser(email, password, name):
    """Validates user register's form information for errors and accordingly
       redirects the page."""

    userCount = session.query(User).filter_by(email=email).one_or_none()
    if userCount:
        return False
    else:
        login_session['provider'] = 'app'
        login_session['name'] = name
        login_session['email'] = email
        newUser = User(name=login_session['name'],
                       password_hash=make_password_hash(email, password),
                       email=login_session['email'])
        session.add(newUser)
        session.commit()
        login_session['user_id'] = getUserID(email)
        return True


def createUser(login_session):
    """Writes new user info in database using login_session's info."""

    email = login_session['email']
    newUser = User(name=login_session['name'],
                   password_hash=make_password_hash(email, email),
                   email=email)
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=email).one_or_none()
    return user.id


def getUserInfo(user_id):
    """Returns user info using passed parameter after fetching from
       database."""

    user = session.query(User).filter_by(id=user_id).one_or_none()
    return user


def getUserID(email):
    """Returns user id using passed parameter after fetching from database."""

    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    """Handler for DISCONNECTING from google."""

    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['name']
        del login_session['email']
        del login_session['image_url']

        response = make_response(json.dumps('Successfully logged out.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON APIs to view Category Information


@app.route('/bot/<int:bot_id>/chat/JSON', methods=['GET', 'POST'])
def chatJSON(bot_id):
    """Generates JSON for game_items of passed category_id."""

    category = session.query(Category).filter_by(id=category_id).one_or_none()
    game_items = session.query(Game).filter_by(category_id=category_id).all()
    return jsonify(GameItems=[i.serialize for i in game_items])


@app.route('/bot/<int:bot_id>/JSON')
def botItemJSON(bot_id):
    """Generates JSON for specified bot."""

    bot_item = session.query(Bot).filter_by(id=bot_id).one_or_none()
    return jsonify(bot_item=bot_item.serialize)


@app.route('/bot/JSON')
def botJSON():
    """Generates JSON for all bots."""

    bots = session.query(Bot).all()
    return jsonify(categories=[r.serialize for r in bots])


# Show HOME page
@cookie_check
@app.route('/')
def showHome():
    """Handler for Home page which displays welcome message."""

    if 'user_id' in login_session:
        return render_template('home.html',
                               menuTitle='Home',
                               menuId='#menuHome',
                               menuColor='w3-col-grey',
                               buttonColor='w3-button-col-grey',
                               textColor='w3-text-col-black',
                               colorHex='#CCCCCC',
                               session=login_session)
    else:
        return render_template('home.html',
                               menuTitle='Home',
                               menuId='#menuHome',
                               menuColor='w3-col-grey',
                               buttonColor='w3-button-col-grey',
                               textColor='w3-text-col-black',
                               colorHex='#CCCCCC')

# Show CHATBOTS (MAIN) page


@cookie_check
@app.route('/chatbots', methods=['GET', 'POST'])
def showChatbots00():
    """Handler for Chatbots page which displays created bots."""

    if request.method == 'POST':
        actionType = request.form['actionType']

        page = int(request.form['botPage'])
        rLimit = 2.0
        pLimit = 3
        start = (page - 1) * rLimit

        if actionType == 'botBrowse':
            if 'user_id' in login_session:
                browse_data = session.query(Bot).\
                    filter_by(bot_availability='N').\
                    order_by(desc(Bot.bot_views)).\
                    offset(start).limit(pLimit).\
                    all()

                count_data = session.query(Bot).\
                    filter_by(bot_availability='N').\
                    count()
            else:
                browse_data = session.query(Bot).\
                    filter_by(bot_availability='N').\
                    order_by(desc(Bot.bot_views)).\
                    offset(start).limit(pLimit).\
                    all()

                count_data = session.query(Bot).\
                    filter_by(bot_availability='N').\
                    count()

        if actionType == 'botSearch':
            if 'user_id' in login_session:
                browse_data = session.query(Bot).\
                    filter(Bot.bot_name.ilike("%" + request.form['botPattern'] + "%")).\
                    filter_by(bot_availability='N').\
                    order_by(desc(Bot.bot_views)).\
                    offset(start).limit(pLimit).\
                    all()

                count_data = session.query(Bot).\
                    filter_by(bot_availability='N').\
                    filter(Bot.bot_name.ilike("%" + request.form['botPattern'] + "%")).\
                    count()
            else:
                browse_data = session.query(Bot).\
                    filter(Bot.bot_name.ilike("%" + request.form['botPattern'] + "%")).\
                    filter_by(bot_availability='N').\
                    order_by(desc(Bot.bot_views)).\
                    offset(start).limit(pLimit).\
                    all()

                count_data = session.query(Bot).\
                    filter(Bot.bot_name.ilike("%" + request.form['botPattern'] + "%")).\
                    filter_by(bot_availability='N').\
                    count()

        last = int(ceil(count_data / rLimit))            
        
        if count_data > 0:
            response = ''

            for browse_row in browse_data:
                response += "<a href='/chatbots/%d/chat'>" % browse_row.bot_id
                response += "<div class='w3-botBox w3-card-2 w3-margin'>"
                response += "<label hidden value='%d' id='botId'></label>" % browse_row.bot_id
                response += "<div class='w3-border w3-center w3-padding'><img class='w3-center-content w3-card-2 w3-avtaar w3-light-red' src='%s'></div>" % browse_row.bot_image
                response += "<div class='w3-border w3-custom-font w3-center'>[ %s ]</div>" % browse_row.bot_name
                response += "</div></a>"

                response += show_pagination00(0, page, last, pLimit)

            return response

        else:
            return "<h2 class='w3-center w3-text-col-red '>No bots to display...</h2>"

    elif 'user_id' in login_session:
        return render_template('chatbots00.html',
                               menuTitle='ChatBots',
                               menuId='#menuChatBots',
                               menuColor='w3-col-red',
                               buttonColor='w3-button-col-red',
                               textColor='w3-text-col-red',
                               colorHex='#E74C3C',
                               session=login_session)
    else:
        return render_template('chatbots00.html',
                               menuTitle='ChatBots',
                               menuId='#menuChatBots',
                               menuColor='w3-col-red',
                               buttonColor='w3-button-col-red',
                               textColor='w3-text-col-red',
                               colorHex='#E74C3C')

# Show CHATBOTS (CHAT) page


@cookie_check
@app.route('/chatbots/<int:bot_id>/chat', methods=['GET', 'POST'])
def showChatbots01(bot_id):
    """Handler for Chatbots page which displays created bots."""

    botInfo = session.query(Bot).filter_by(bot_id=bot_id).one_or_none()

    if request.method == 'POST':
        messageType = request.form['messageType']

        if messageType == 'Q':
            messageString = (request.form['messageString']).lower().strip()
            botId = request.form['botId']

            rows_TypeQ = session.query(Knowledge).\
                filter_by(bot_id=botId).\
                filter_by(type='Q').\
                filter_by(pattern=messageString).\
                order_by(func.random()).\
                first()

            rows_TypeR = session.query(Knowledge).\
                filter_by(bot_id=botId).\
                filter_by(type='R').\
                filter_by(pattern=messageString).\
                order_by(func.random()).\
                first()

            if rows_TypeQ:
                responseList = (rows_TypeQ.template).splitlines()
                response = random.choice(responseList)

            else:
                if botInfo.bot_add:
                    newKnowledge = Knowledge(bot_id=botInfo.bot_id,
                                             type='Q',
                                             pattern=messageString,
                                             created_date=func.now())
                    session.add(newKnowledge)
                    session.commit()

                if rows_TypeR:
                    responseList = (rows_TypeR.template).splitlines()
                    response = random.choice(responseList)

                else:
                    responseList = ["Huh.", "What?", "...", "(0?0) What?"]
                    response = random.choice(responseList)

            '''log_conversation($_BOT_ID, "messageType", $_MESSAGE, $_RESPONSE)'''
            return response

        elif messageType == 'G':
            botId = request.form['botId']

            rows_TypeG = session.query(Knowledge).\
                filter_by(bot_id=botId).\
                filter_by(type='G').\
                order_by(func.random()).\
                first()

            if rows_TypeG:
                responseList = (rows_TypeG.template).splitlines()
                response = random.choice(responseList)

            else:
                responseList = ["Hi", "Hello.", "Hey", "(0U0)/ Hi"]
                response = random.choice(responseList)

            '''log_conversation($_BOT_ID, "G", '', $_RESPONSE);'''
            return response

        elif messageType == 'E':
            botId = request.form['botId']

            '''log_conversation($_BOT_ID, "E", '', '');'''

    elif 'user_id' in login_session and botInfo:
        return render_template('chatbots01.html',
                               menuTitle='ChatBots',
                               menuId='#menuChatBots',
                               menuColor='w3-col-red',
                               buttonColor='w3-button-col-red',
                               textColor='w3-text-col-red',
                               colorHex='#E74C3C',
                               session=login_session,
                               botInfo=botInfo)
    elif botInfo:
        return render_template('chatbots01.html',
                               menuTitle='ChatBots',
                               menuId='#menuChatBots',
                               menuColor='w3-col-red',
                               buttonColor='w3-button-col-red',
                               textColor='w3-text-col-red',
                               colorHex='#E74C3C',
                               botInfo=botInfo)
    else:
        return render_template('error.html',
                               menuTitle='ChatBots',
                               menuId='#menuChatBots',
                               menuColor='w3-col-red',
                               buttonColor='w3-button-col-red',
                               textColor='w3-text-col-red',
                               colorHex='#E74C3C',
                               header='Sorry',
                               content='This bot does not exist.',
                               session=login_session)


# Show GUIDE page
@cookie_check
@app.route('/guide')
def showGuide():
    """Handler for Home page which displays welcome message."""

    if 'user_id' in login_session:
        return render_template('guide.html',
                               menuTitle='Guide',
                               menuId='#menuGuide',
                               menuColor='w3-col-grey',
                               buttonColor='w3-button-col-blue',
                               textColor='w3-text-col-blue',
                               colorHex='#3498DB',
                               session=login_session)
    else:
        return render_template('guide.html',
                               menuTitle='Guide',
                               menuId='#menuGuide',
                               menuColor='w3-col-blue',
                               buttonColor='w3-button-col-blue',
                               textColor='w3-text-col-blue',
                               colorHex='#3498DB')

# Show FAQs page


@cookie_check
@app.route('/faq')
def showFAQs():
    """Handler for Home page which displays welcome message."""

    if 'user_id' in login_session:
        return render_template('faq.html',
                               menuTitle='FAQs',
                               menuId='#menuFaq',
                               menuColor='w3-col-grey',
                               buttonColor='w3-button-col-green',
                               textColor='w3-text-col-green',
                               colorHex='#27AE60',
                               session=login_session)
    else:
        return render_template('faq.html',
                               menuTitle='FAQs',
                               menuId='#menuFaq',
                               menuColor='w3-col-grey',
                               buttonColor='w3-button-col-green',
                               textColor='w3-text-col-green',
                               colorHex='#27AE60')

# Show CONTACT page


@cookie_check
@app.route('/contact')
def showContact():
    """Handler for Home page which displays welcome message."""

    if 'user_id' in login_session:
        return render_template('contact.html',
                               menuTitle='Contact',
                               menuId='#menuContact',
                               menuColor='w3-col-yellow',
                               buttonColor='w3-button-col-orange',
                               textColor='w3-text-col-orange',
                               colorHex='#F39C12',
                               session=login_session)
    else:
        return render_template('contact.html',
                               menuTitle='Contact',
                               menuId='#menuContact',
                               menuColor='w3-col-yellow',
                               buttonColor='w3-button-col-orange',
                               textColor='w3-text-col-orange',
                               colorHex='#F39C12')


# Show EMBED page
@cookie_check
@app.route('/embed')
def showEmbed():
    """Handler for Home page which displays welcome message."""

    if 'user_id' in login_session:
        return render_template('embed.html',
                               menuTitle='Embed',
                               menuId='#menuEmbed',
                               menuColor='w3-col-darkorange',
                               buttonColor='w3-button-col-darkorange',
                               textColor='w3-text-col-darkorange',
                               colorHex='#E67E22',
                               session=login_session)
    else:
        return render_template('embed.html',
                               menuTitle='Embed',
                               menuId='#menuEmbed',
                               menuColor='w3-col-darkorange',
                               buttonColor='w3-button-col-darkorange',
                               textColor='w3-text-col-darkorange',
                               colorHex='#E67E22')

# Show TEACH page


@cookie_check
@app.route('/teach', methods=['GET', 'POST'])
def showTeach():
    """Handler for Chatbots page which displays created bots."""

    if request.method == 'POST':
        actionType = request.form['actionType']

        if actionType == 'sBrowse':
            page = int(request.form['qPage'])
            rLimit = 2.0
            pLimit = 3
            start = (page - 1) * rLimit
            
            browse_data = session.query(Knowledge).\
                filter(Knowledge.pattern.ilike("%" + request.form['qPattern'] + "%")).\
                filter_by(bot_id=login_session['user_id']).\
                order_by(desc(Knowledge.created_date)).\
                offset(start).limit(pLimit).\
                all()

            count_data = session.query(Knowledge).\
                filter(Knowledge.pattern.ilike("%" + request.form['qPattern'] + "%")).\
                filter_by(bot_id=login_session['user_id']).\
                count()
            
            last = int(ceil(count_data / rLimit))     
            
            if count_data > 0:
                response = "<table class='w3-qBox w3-padding-bottom w3-round'>"

                for browse_row in browse_data:
                    response += "<tr><td class='w3-border w3-round w3-full-width'>"

                    if browse_row.template:
                        response += '[A]'
                    else:
                        response += '[U]'

                    response += "[<span id='qType'>%s</span>]\<span id='qChanged'></span><span id='qPattern'>%s</span>" % (
                        browse_row.type, browse_row.pattern)
                    response += "<label hidden value='%d' id='qId'></label>" % browse_row.id
                    response += "<button onclick='qAction (0, this)' class='w3-right w3-xlarge w3-qButton'>[ <i class='fa fa-trash'></i> ]</button>"
                    response += "<button onclick='qAction (1, this)' class='w3-right w3-xlarge w3-qButton'>[ <i class='fa fa-pencil'></i> ]</button>"
                    response += "<button onclick='qAction (2, this)' class='w3-right w3-xlarge w3-qButton'>[ <i class='fa fa-save'></i> ]</button>"
                    response += "<textarea hidden id='qTemplate' oninput='qAction (3, this)' class='w3-qTemplate w3-padding w3-border w3-round' autocomplete='off' autofocus placeholder='type response...'>%s</textarea>" % browse_row.template
                    response += "</td></tr>"

                response += show_pagination01('sAction', page, last, pLimit)

                response += "</table>"
                
                return response
            else:
                return "<h2 class='w3-center w3-text-col-darkblue'>No results to display...</h2>"

        elif actionType == 'iInfo':
            count_typeA = session.query(Knowledge).\
                filter(Knowledge.pattern.isnot(None)).\
                filter_by(bot_id=login_session['user_id']).\
                count()

            count_typeU = session.query(Knowledge).\
                filter(Knowledge.pattern.is_(None)).\
                filter_by(bot_id=login_session['user_id']).\
                count()

            count_typeR = session.query(Knowledge).\
                filter_by(bot_id=login_session['user_id']).\
                filter_by(type='R').\
                count()

            count_typeQ = session.query(Knowledge).\
                filter_by(bot_id=login_session['user_id']).\
                filter_by(type='Q').\
                count()

            count_typeA = float(count_typeA)
            count_typeU = float(count_typeU)
            count_typeQ = float(count_typeQ)
            count_typeR = float(count_typeR)

            count_total = count_typeA + count_typeU + count_typeQ + count_typeR

            if count_total == 0:
                count_total = 1

            response = "<div class='w3-margin-bottom w3-center-content'>"
            response += "<span>< TypeA.Questions > <%.2f%%> <%d> </span><br>" % (
                (count_typeA / count_total) * 100, count_typeA)
            response += "<span>< TypeU.Questions > <%.2f%%> <%d> </span><br>" % (
                (count_typeU / count_total) * 100, count_typeU)
            response += "<span>< TypeQ.Questions > <%.2f%%> <%d> </span><br>" % (
                (count_typeQ / count_total) * 100, count_typeQ)
            response += "<span>< TypeR.Questions > <%.2f%%> <%d> </span><br>" % (
                (count_typeR / count_total) * 100, count_typeR)
            response += "</div>"

            return response

        elif actionType == 'aSave':
            newKnowledge = Knowledge(bot_id=login_session['user_id'],
                                     type=request.form['qType'],
                                     pattern=request.form['qPattern'],
                                     template=request.form['qTemplate'],
                                     created_date=func.now())
            session.add(newKnowledge)
            session.commit()

            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

        elif actionType == 'qSave':
            editKnowledge = session.query(Knowledge).\
                filter_by(id=request.form['qId']).\
                one_or_none()

            editKnowledge.pattern = request.form['qPattern']
            editKnowledge.template = request.form['qTemplate']

            session.add(editKnowledge)
            session.commit()

            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

        elif actionType == 'qDelete':
            deleteKnowledge = session.query(Knowledge).\
                filter_by(id=int(request.form['qId'])).\
                one_or_none()

            session.delete(deleteKnowledge)
            session.commit()
            
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

        elif actionType == 'bBrowse':

            page = int(request.form['qPage'])
            type01 = request.form['qType'][0]
            type02 = request.form['qType'][1]
            rLimit = 2.0
            pLimit = 3
            start = (page - 1) * rLimit

            if type01 == '*' and type02 == '*':
                browse_data = session.query(Knowledge).\
                    filter_by(bot_id=login_session['user_id']).\
                    order_by(desc(Knowledge.created_date)).\
                    offset(start).limit(pLimit).\
                    all()

                count_data = session.query(Knowledge).\
                    filter_by(bot_id=login_session['user_id']).\
                    count()

            elif type01 == 'A' and type02 == '*':
                browse_data = session.query(Knowledge).\
                    filter(Knowledge.pattern.isnot(None)).\
                    filter_by(bot_id=login_session['user_id']).\
                    order_by(desc(Knowledge.created_date)).\
                    offset(start).limit(pLimit).\
                    all()

                count_data = session.query(Knowledge).\
                    filter(Knowledge.pattern.is_(None)).\
                    filter_by(bot_id=login_session['user_id']).\
                    count()

            elif type01 == 'U' and type02 == '*':
                browse_data = session.query(Knowledge).\
                    filter(Knowledge.pattern.is_(None)).\
                    filter_by(bot_id=login_session['user_id']).\
                    order_by(desc(Knowledge.created_date)).\
                    offset(start).limit(pLimit).\
                    all()

                count_data = session.query(Knowledge).\
                    filter(Knowledge.pattern.isnot(None)).\
                    filter_by(bot_id=login_session['user_id']).\
                    count()

            elif type01 == '*' and not type02 == '*':
                browse_data = session.query(Knowledge).\
                    filter_by(bot_id=login_session['user_id']).\
                    filter_by(type=type02).\
                    order_by(desc(Knowledge.created_date)).\
                    offset(start).limit(pLimit).\
                    all()

                count_data = session.query(Knowledge).\
                    filter_by(bot_id=login_session['user_id']).\
                    filter_by(type=type02).\
                    count()

            elif type01 == 'A' and not type02 == '*':
                browse_data = session.query(Knowledge).\
                    filter(Knowledge.pattern.isnot(None)).\
                    filter_by(bot_id=login_session['user_id']).\
                    filter_by(type=type02).\
                    order_by(desc(Knowledge.created_date)).\
                    offset(start).limit(pLimit).\
                    all()

                count_data = session.query(Knowledge).\
                    filter(Knowledge.pattern.isnot(None)).\
                    filter_by(bot_id=login_session['user_id']).\
                    filter_by(type=type02).\
                    count()

            elif type01 == 'U' and not type02 == '*':
                browse_data = session.query(Knowledge).\
                    filter(Knowledge.pattern.is_(None)).\
                    filter_by(bot_id=login_session['user_id']).\
                    filter_by(type=type02).\
                    order_by(desc(Knowledge.created_date)).\
                    offset(start).limit(pLimit).\
                    all()

                count_data = session.query(Knowledge).\
                    filter(Knowledge.pattern.is_(None)).\
                    filter_by(bot_id=login_session['user_id']).\
                    filter_by(type=type02).\
                    count()

            last = int(ceil(count_data / rLimit))        
            
            if count_data > 0:
                response = "<table class='w3-qBox w3-padding-bottom w3-round'>"

                for browse_row in browse_data:
                    response += "<tr><td class='w3-border w3-round w3-full-width'>"

                    if browse_row.template:
                        response += '[A]'
                    else:
                        response += '[U]'

                    response += "[<span id='qType'>%s</span>]\<span id='qChanged'></span><span id='qPattern'>%s</span>" % (
                        browse_row.type, browse_row.pattern)
                    response += "<label hidden value='%d' id='qId'></label>" % browse_row.id
                    response += "<button onclick='qAction(0, this)' class='w3-right w3-xlarge w3-qButton'>[ <i class='fa fa-trash'></i> ]</button>"
                    response += "<button onclick='qAction(1, this)' class='w3-right w3-xlarge w3-qButton'>[ <i class='fa fa-pencil'></i> ]</button>"
                    response += "<button onclick='qAction(2, this)' class='w3-right w3-xlarge w3-qButton'>[ <i class='fa fa-save'></i> ]</button>"
                    response += "<textarea hidden id='qTemplate' oninput='qAction (3, this)' class='w3-qTemplate w3-padding w3-border w3-round' autocomplete='off' autofocus placeholder='type response...'>%s</textarea>" % browse_row.template
                    response += "</td></tr>"

                response += show_pagination01('bAction', page, last, pLimit)

                response += "</table>"

                return response
            else:
                return "<h2 class='w3-center w3-text-col-darkblue '>No results to display...</h2>"

        elif actionType == 'lBrowse':
            page = int(request.form['qPage'])
            rLimit = 2.0
            pLimit = 3
            start = (page - 1) * rLimit

            browse_data = session.query(Chatlog).\
                filter_by(bot_id=login_session['user_id']).\
                order_by(desc(Chatlog.created_date)).\
                offset(start).limit(pLimit).\
                all()

            count_data = session.query(Chatlog).\
                filter_by(bot_id=login_session['user_id']).\
                count()

            last = int(ceil(count_data / rLimit))

            if count_data > 0:
                response = "<table class='w3-qBox w3-padding-bottom w3-round'>"

                for browse_row in browse_data:
                    response += "<tr><td class='w3-border w3-round w3-full-width'>"
                    response += "[<span id='qType'>%s</span>]\<span id='qChanged'></span><span id='qPattern'>%s</span>" % (
                        browse_row.created_date, browse_row.client_ip)
                    response += "<label hidden value='%d' id='qId'></label>" % browse_row.id
                    response += "<button onclick='qAction (5, this)' class='w3-right w3-xlarge w3-qButton'>[ <i class='fa fa-trash'></i> ]</button>"
                    response += "<button onclick='qAction (1, this)' class='w3-right w3-xlarge w3-qButton'>[ <i class='fa fa-level-down'></i> ]</button>"
                    response += "<button onclick='qAction (4, this)' class='w3-right w3-xlarge w3-qButton'>[ <i class='fa fa-download'></i> ]</button>"
                    response += "<textarea hidden id='qTemplate' class='w3-qTemplate w3-padding w3-border w3-round' autocomplete='off' autofocus placeholder='empty...'>%s</textarea>" % browse_row.bot_log
                    response += "</td></tr>"
         
                response += show_pagination01('lAction', page, last, pLimit)

                response += "</table>"

                return response
            else:
                return "<h2 class='w3-center w3-text-col-darkblue'>No results to display...</h2>"

        elif actionType == 'lDelete':
            deleteChatlog = session.query(Chatlog).\
                filter_by(id=request.form['qId']).\
                one_or_none()

            session.delete(deleteChatlog)
            session.commit()

            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

    elif 'user_id' in login_session:
        return render_template('teach.html',
                               menuTitle='Teach',
                               menuId='#menuTeach',
                               menuColor='w3-col-darkblue',
                               buttonColor='w3-button-col-darkblue',
                               textColor='w3-text-col-darkblue',
                               colorHex='#2980B9',
                               session=login_session)
    else:
        flash("you must be logged in first.")
        return redirect(url_for('showLogin'))


# Show CHAT page
@cookie_check
@app.route('/chat', methods=['GET', 'POST'])
def showChat():
    """Handler for Chatbots page which displays created bots."""

    botInfo = session.query(Bot).\
        filter_by(bot_id=login_session['user_id']).\
        one_or_none()

    if 'user_id' in login_session:
        if request.method == 'POST':
            messageType = request.form['messageType']

            if messageType == 'Q':
                messageString = (request.form['messageString']).lower().strip()

                rows_TypeQ = session.query(Knowledge).\
                    filter(Knowledge.pattern.isnot(None)).\
                    filter_by(bot_id=login_session['user_id']).\
                    filter_by(type='Q').\
                    filter_by(pattern=messageString).\
                    order_by(func.random()).\
                    first()

                rows_TypeR = session.query(Knowledge).\
                    filter_by(bot_id=login_session['user_id']).\
                    filter_by(type='R').\
                    filter_by(pattern=messageString).\
                    order_by(func.random()).\
                    first()

                if rows_TypeQ:
                    responseList = (rows_TypeQ.template).splitlines()
                    response = random.choice(responseList)

                else:
                    if botInfo.bot_add:
                        newKnowledge = Knowledge(bot_id=botInfo.bot_id,
                                                 type='Q',
                                                 pattern=messageString,
                                                 created_date=func.now())
                        session.add(newKnowledge)
                        session.commit()

                    if rows_TypeR:
                        responseList = (rows_TypeR.template).splitlines()
                        response = random.choice(responseList)

                    else:
                        responseList = ["Huh.", "What?", "...", "(0?0) What?"]
                        response = random.choice(responseList)

                log_conversation(botInfo.bot_id, messageType, messageString, response)
                return response

            elif messageType == 'G':
                rows_TypeG = session.query(Knowledge).\
                    filter(Knowledge.pattern.isnot(None)).\
                    filter_by(bot_id=login_session['user_id']).\
                    filter_by(type='G').\
                    order_by(func.random()).\
                    first()

                if rows_TypeG:
                    responseList = (rows_TypeG.template).splitlines()
                    response = random.choice(responseList)

                else:
                    responseList = ["Hi", "Hello.", "Hey", "(0U0)/ Hi"]
                    response = random.choice(responseList)

                log_conversation(botInfo.bot_id, "G", '', response)
       
                return response

            elif messageType == 'E':
                log_conversation(botInfo.bot_id, "E", '', '')

        else:
            return render_template('chat.html',
                                   menuTitle='Chat',
                                   menuId='#menuChat',
                                   menuColor='w3-col-darkred',
                                   buttonColor='w3-button-col-darkred',
                                   textColor='w3-text-col-darkred',
                                   colorHex='#C0392B',
                                   botInfo=botInfo,
                                   session=login_session)
    else:
        flash("you must be logged in first.")
        return redirect(url_for('showLogin'))


@app.route('/logout')
def showLogout():
    """DISCONNECTS the user based on provider."""

    if 'provider' in login_session:

        if 'user_id' in login_session:
            del login_session['name']
        if 'email' in login_session:
            del login_session['email']
        if 'user_id' in login_session:
            del login_session['user_id']

        flash("you have successfully been logged out.")
        response = make_response(redirect(url_for('showHome')))
        response.set_cookie('user_id', expires=0)
        return response
    else:
        flash("you were not logged in.")
        return redirect(url_for('showHome'))

if __name__ == '__main__':
    app.secret_key = get_secret()
    app.debug = True
    app.run(port=port)
