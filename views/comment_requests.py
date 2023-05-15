import sqlite3
import json
from models import Comment, User

COMMENTS = [
  {
    "id": 1,
    "author_id": 1,
    "post_id": 1,
    "content": "This is a comment for a post."
  },
  {
    "id": 2,
    "author_id": 2,
    "post_id": 2,
    "content": "This is a comment for another post."
  },
  {
    "id": 3,
    "author_id": 3,
    "post_id": 3,
    "content": "This is a comment for yet another post."
  }
]

def get_all_comments():
    """To GET all comments"""
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.author_id,
            c.post_id,
            c.content,
            u.id user_id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.created_on,
            u.active
        FROM Comments c
        JOIN Users u
            ON u.id = c.author_id            
        """)

        # Initialize an empty list to hold all comment representations
        comments = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a comment instance from the current row
            comment = Comment(row['id'],
                              row['author_id'],
                              row['post_id'],
                              row['content'],)

            # Create a user instance from the current row
            user = User(row['user_id'],
                        row['first_name'],
                        row['last_name'],
                        row['email'],
                        row['bio'],
                        row['username'],
                        row['password'],
                        row['created_on'],
                        row['active'])

            # Add the dictionary representation of the user to the comment
            comment.user = user.__dict__

            # Add the dictionary representation of the comment to the list
            comments.append(comment.__dict__)

    return comments

def get_single_comment(id):
    """To GET a single comment"""
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            c.id,
            c.author_id,
            c.post_id,
            c.content,
            u.id user_id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.created_on,
            u.active
        FROM Comments c
        JOIN Users u
            ON u.id = c.author_id
        WHERE c.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create a comment instance from the current row
        comment = Comment(data['id'],
                          data['author_id'],
                          data['post_id'],
                          data['content'],)

        user = User(data['user_id'],
                    data['first_name'],
                    data['last_name'],
                    data['email'],
                    data['bio'],
                    data['username'],
                    data['password'],
                    data['created_on'],
                    data['active'])

        comment.user = user.__dict__

        return comment.__dict__

def create_comment(new_comment):
    """To POST a comment"""
      # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments
            ( author_id, post_id, content )
        VALUES
            ( ?, ?, ?);
        """, (new_comment['author_id'],
              new_comment['post_id'],
              new_comment['content'], ))
        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the comment dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_comment['id'] = id


    return json.dumps(new_comment)

def delete_comment(id):
    """To DELETE a comment"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Comments
        WHERE id = ?
        """, (id, ))

def update_comment(id, new_comment):
    """To PUT a comment"""
      # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Comments
            SET
                author_id = ?,
                post_id = ?,
                content = ?
        WHERE id=?
        """, (new_comment['author_id'],
              new_comment['post_id'],
              new_comment['content'],
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
