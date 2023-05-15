import sqlite3
import json
from datetime import datetime
from models import User

USERS = [
    {
        "id": 1,
        "first_name": "Charles",
        "last_name": "Bridgers",
        "email": "mcmaster@gmail.com",
        "bio": "This is your favorite local hip-hop host!",
        "username": "c4theexplosive",
        "password": "password",
        "created_on": "8/6/2022",
        "active": False
    },
    {
        "id": 2,
        "first_name": "Instructor",
        "last_name": "Danny",
        "email": "pythonnerd12@gmail.com",
        "bio": "Junior instructor for NSS!",
        "username": "dantheman",
        "password": "password",
        "created_on": "6/12/2022",
        "active": False
    },
    {
        "id": 3,
        "first_name": "Angie",
        "last_name": "Gonzalez",
        "email": "eagleeyeangie@gmail.com",
        "bio": "Music theory and coding wiz!",
        "username": "eagleeyeangie",
        "password": "password",
        "created_on": "2/4/2023",
        "active": False
    }
]

def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's 
        id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select id, username
            from Users
            where username = ?
            and password = ?
        """, (user['username'], user['password']))

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {
                'valid': True,
                'token': user_from_db['id']
            }
        else:
            response = {
                'valid': False
            }

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            user['first_name'],
            user['last_name'],
            user['username'],
            user['email'],
            user['password'],
            user['bio'],
            datetime.now()
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })

def get_all_users():
    """DOCSTRING
    """
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.created_on,
            u.active
        FROM Users u
        """)

        # Initialize an empty list to hold all animal representations
        users = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            user = User(row['id'], row['first_name'], row['last_name'], row['email'],
                            row['bio'], row['username'],
                            row['password'], row['created_on'], row['active'])

            users.append(user.__dict__)
            # see the notes below for an explanation on this line of code.

    return users

def get_single_user(id):
    """DOCSTRING
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.created_on,
            u.active
        FROM Users u
        WHERE u.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        user = User(data['id'], data['first_name'], data['last_name'], data['email'],
                            data['bio'], data['username'],
                            data['password'], data['created_on'], data['active'])

        return user.__dict__

def update_user(id, new_user):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Users
            SET
                first_name = ?,
                last_name = ?,
                email = ?,
                bio = ?,
                username = ?,
                password = ?,
                created_on = ?,
                active = ?
        WHERE id = ?
        """, (new_user['first_name'], new_user['last_name'], new_user['email'],
              new_user['bio'], new_user['username'], new_user['password'],
              new_user['created_on'], new_user['active'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def delete_user(id):
    # Initial -1 value for animal index, in case one isn't found
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Users
        WHERE id = ?
        """, (id, ))
