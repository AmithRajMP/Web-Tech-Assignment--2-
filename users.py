"""
Created on Mar 26, 2012

@author: Amith Raj
"""
from database import password_hash
import bottle
from bottle import request
# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'


def check_login(db, usernick, password):
    """returns True if password matches stored"""
    cursor = db.cursor()
    query = """SELECT password FROM users WHERE nick=?"""
    cursor.execute(query, [usernick])
    """Since usernick is a foreign key of nick from 'user' table, it can be used as parameter for 
    nick in the above query"""
    enpass = cursor.fetchone()
    if enpass is None:
        return False
    else:
        plaintext = enpass[0]
        hash = password_hash(password)
        if hash == plaintext:
            return True
        else:
            return False


def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """
    result = exist_user(db, usernick)
    if result is False:
        return None
        """If user doesnt exist return None and end. Else continue"""
    else:
        cursor = db.cursor()
        sid_query = """SELECT sessionid FROM sessions WHERE usernick=?"""
        cursor.execute(sid_query, [usernick])
        sessid = cursor.fetchone()
        """If session doesnt exist, create a new one. If it exists return the sessionid"""
        if sessid is None:
            """Calling insert_session to insert a session and returns the session id"""
            sessionid = insert_session(db, usernick)
        else:
            sessionid = sessid[0]

        bottle.response.set_cookie(COOKIE_NAME, sessionid)
        return sessionid


def insert_session(db, usernick):
    """Inserts session if session doesnt exist and returns the sessionid inserted"""
    cursor = db.cursor()
    insert = """INSERT INTO sessions (sessionid, usernick) values (?,?)"""
    sessionid = usernick + "session"
    cursor.execute(insert, [sessionid, usernick])
    db.commit()
    return sessionid


def exist_user(db, usernick):
    """Returns true if user exists"""
    cursor = db.cursor()
    query = """SELECT avatar FROM users WHERE nick=?"""
    cursor.execute(query, [usernick])
    user_exists = cursor.fetchone()
    if user_exists is None:
        return False
    else:
        return True


def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cursor = db.cursor()
    delete = """DELETE FROM sessions WHERE usernick=?"""
    cursor.execute(delete, [usernick])
    db.commit()


def session_user(db):
    """Retrieve the  sessionid from the cookie, if session doesnt exist return None.
    If session exists, find the owner of the session and return the username"""
    sessionid = request.get_cookie(COOKIE_NAME)
    """Retrieving the sessionid from the cookie"""
    if sessionid is None:
        return None
    else:
        cursor = db.cursor()
        query = """SELECT usernick from sessions WHERE sessionid=?"""
        cursor.execute(query, [sessionid])
        session = cursor.fetchone()
        if session:
            usernick = session[0]
            return usernick
        else:
            return None


def get_avatar(db, usernick):
    """Returns the avatar of the logged in user"""
    sessionid = request.get_cookie(COOKIE_NAME)
    """Retrieving the sessionid from the cookie"""
    if sessionid is None:
        return None
    else:
        cursor = db.cursor()
        query = """SELECT avatar FROM users WHERE nick=?"""
        cursor.execute(query, [usernick])
        display_picture = cursor.fetchone()
        if display_picture:
            avatar = display_picture[0]
            print(avatar)
            return avatar
        else:
            return None


