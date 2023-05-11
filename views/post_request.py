import sqlite3
import json
from models import Posts

POSTS = [
    {
        "id": 1,
        "user_id": 1,
        "title": "Love Effects",
        "publication_date": 5/9/2023,
        "content": "Love Makes Everything Better"
    },
    {
        "id": 2,
        "user_id": 2,
        "title": "Hate Effects",
        "publication_date": 5/10/2023,
        "content": "Hate Makes Everything Worst"
    },
    {
        "id": 3,
        "user_id": 1,
        "title": "I Need Food",
        "publication_date": 5/11/2023,
        "content": "Food Makes Everything Better"
    },
    {
        "id": 4,
        "user_id": 2,
        "title": "I Adore Water",
        "publication_date": 5/12/2023,
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
            p.content,
            u.first_name user_first_name,
            u.last_name user_last_name,    
        FROM posts p
        JOIN User u
            ON u.id = p.user_id
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
            #     row['id'], row['user_first_name'], row['user_last_name'])

            # # Add the dictionary representation of the location to the animal
            # post.user = user.__dict__

            # Add the dictionary representation of the animal to the list
            posts.append(post.__dict__)

    return posts


def get_single_post(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
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
        FROM post p
        WHERE p.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        post = Posts(data['id'], data['user_id'], data['title'],
                     data['publication_date'], data['content'])

        return post.__dict__
