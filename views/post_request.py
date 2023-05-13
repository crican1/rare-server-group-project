import sqlite3
import json
from models import Posts, User

POSTS = [
    {
        "id": 1,
        "user_id": 1,
        "title": "Love Effects",
        "publication_date": "5/9/2023",
        "content": "Love Makes Everything Better"
    },
    {
        "id": 2,
        "user_id": 2,
        "title": "Hate Effects",
        "publication_date": "5/10/2023",
        "content": "Hate Makes Everything Worst"
    },
    {
        "id": 3,
        "user_id": 3,
        "title": "I Need Food",
        "publication_date": "5/11/2023",
        "content": "Food Makes Everything Better"
    },
    {
        "id": 4,
        "user_id": 4,
        "title": "I Adore Water",
        "publication_date": "5/12/2023",
        "content": "Water Makes Everything Wetter"
    }
]


def get_all_posts():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.title,
            p.publication_date,
            p.content    
        FROM Posts p
        """)

        # Initialize an empty list to hold all animal representations
        posts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            post = Posts(row['id'], row['user_id'], row['title'], row['publication_date'],
                            row['content'])

            # Create a Location instance from the current row
            # user = User(
            #     row['id'], ['user_first_name'], row['user_last_name'])

            # # Add the dictionary representation of the location to the animal
            # post.user = user.__dict__

            # Add the dictionary representation of the animal to the list
            posts.append(post.__dict__)

    return posts


def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.title,
            p.publication_date,
            p.content
        FROM Posts p
        WHERE p.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        post = Posts(data['id'], data['user_id'], data['title'],
                     data['publication_date'], data['content'])

        return post.__dict__


def create_post(new_post):
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, title, publication_date, content )
        VALUES
            ( ?, ?, ?, ? );
        """, (new_post['user_id'],
              new_post['title'],
              new_post['publication_date'],
              new_post['content']))
        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the comment dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['id'] = id

    return json.dumps(new_post)

def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))
        

def update_post(id, new_post):
    """To PUT a post"""
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        # Just use these. It’s a Black Box.
        db_cursor = conn.cursor()
        db_cursor.execute("""
                          UPDATE Posts
                          SET
                          user_id= ?,
                          title= ?,
                          publication_date= ?,
                          content= ?
                          WHERE id=?
                          """, (new_post['user_id'],
                                new_post['title'],
                                new_post['publication_date'],
                                new_post['content'],
                                id, ))
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
