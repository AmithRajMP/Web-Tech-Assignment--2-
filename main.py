__author__ = 'Amith Raj'

from bottle import Bottle, template, static_file
import sqlite3
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

@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')




if __name__ == '__main__':

    from bottle.ext import sqlite
    from database import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
