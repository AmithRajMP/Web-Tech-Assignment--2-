"""
Database Model interface for the COMP249 Web Application assignment

@author: Amith Raj
"""


def position_list(db, limit=10):
    """Return a list of positions ordered by date
    db is a database connection
    return at most limit positions (default 10)

    Returns a list of tuples  (id, timestamp, owner, title, location, company, description)
    """
    cursor = db.cursor()
    query = """SELECT id, 
    timestamp, 
    owner, 
    title, 
    location, 
    company, 
    description 
    FROM positions 
    ORDER BY timestamp 
    DESC LIMIT ?"""
    cursor.execute(query, [limit])
    return cursor.fetchall()


def position_get(db, id):
    """Return the details of the position with the given id
    or None if there is no position with this id

    Returns a tuple (id, timestamp, owner, title, location, company, description)

    """
    cursor = db.cursor()
    query = """SELECT id, 
    timestamp, 
    owner, 
    title, 
    location, 
    company, 
    description 
    FROM positions 
    WHERE id=?"""
    resultset = cursor.execute(query, [id])
    if resultset:
        return cursor.fetchone()
    else:
        return None



def position_add(db, usernick, title, location, company, description):
    """Add a new post to the database.
    The date of the post will be the current time and date.
    Only add the record if usernick matches an existing user

    Return True if the record was added, False if not."""
    cursor = db.cursor()
    query = """SELECT nick FROM users WHERE nick=?"""
    cursor.execute(query, [usernick])
    if cursor.fetchone():
        insert = """INSERT INTO positions (timestamp, 
        owner, title, location, company, description) 
        VALUES (CURRENT_TIMESTAMP,?,?,?,?,?)"""
        cursor.execute(insert, [usernick, title, location, company, description])
        db.commit()
        return True
    else:
        return False




