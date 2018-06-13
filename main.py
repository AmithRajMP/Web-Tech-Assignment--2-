__author__ = 'Amith Raj'

from bottle import Bottle, template, static_file, request, response, redirect
import users
import interface
app = Bottle()


@app.route('/')
def index(db):
    """Passing positions data to the index.html page by calling the position_list function from interface.py
    sending that info to the index.html where it is separated and displayed accordingly.
    Returns the template along with the most recent 10 positions to be displayed in the homepage"""
    position = interface.position_list(db, 10)
    info = {
                'positions': position
            }
    if users.session_user(db):
        """If the user has logged in, then render "login_index" template. 
        Pass the username and avatar of the user to display in the template"""
        return template('login_index', info, user=users.session_user(db),
                        avatar=users.get_avatar(db, users.session_user(db)))
    else:
        return template('index.html', info)


@app.route('/positions/<jobid>')
def expand(db, jobid):
    """Passing position data to the descexpander.html page by calling the position_get function from interface.py
        sending that info to the descexpander.html where it is separated and displayed accordingly.
        Returns the template along with the data of the given job id.
        Page with the full description of the position at the URL /positions/jobid where jobid is the position id."""
    data = {
        'description': interface.position_get(db, jobid)
    }
    return template('descexpander.html', data)


@app.route('/login', method='POST')
def check_login(db):
    """Checking the Username and Password against the user's database
    Generate a session for the user and display index.html, else create a session and redirect to /"""
    user = request.forms.nick
    password = request.forms.password
    if users.check_login(db, user, password) is True:
        users.generate_session(db, user)
        redirect('/')
    else:
        return template("login_error")


@app.route('/post')
def add_database(db):
    """Logged in user can add new positions
    using position_add() from interface.py to add positions"""
    usernick = users.session_user(db)
    title = request.query.title
    location = request.query.location
    company = request.query.company
    description = request.query.description
    interface.position_add(db, usernick, title, location, company, description)
    redirect('/')


@app.route('/logout')
def logout(db):
    """Username is retrieved from the session and
    session will be terminated using the delete_session from users.py"""
    usernick = users.session_user(db)
    users.delete_session(db, usernick)
    redirect('/')


@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':

    from bottle.ext import sqlite
    from database import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
