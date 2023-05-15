import sqlite3
import json
from models import Subscription
from .post_request import get_post_by_user

SUBSCRIPTIONS = [
    {
        "id": 1,
        "follower_id": 1,
        "author_id": 3,
        "created_on": '6/11/2022'
    },
    {
        "id": 2,
        "follower_id": 2,
        "author_id": 3,
        "created_on": '6/12/2022'
    }
]

def get_all_subscriptions():
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
            a.id,
            a.follower_id,
            a.author_id,
            a.created_on
        FROM Subscriptions a
        """)

        # Initialize an empty list to hold all animal representations
        subscriptions = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            subscription = Subscription(row['id'], row['follower_id'],
                                        row['author_id'], row['created_on'])

            subscriptions.append(subscription.__dict__)

    return subscriptions

# Function with a single parameter
def get_single_subscription(id):
    """DOCSTRING
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.follower_id,
            a.author_id,
            a.created_on
        FROM Subscriptions a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        subscription = Subscription(data['id'], data['follower_id'],
                                    data['author_id'], data['created_on'])

        return subscription.__dict__

def create_subscription(new_subscription):
    """DOCSTRING
    """
      # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Subscriptions
            ( author_id, follower_id, created_on )
        VALUES
            ( ?, ?, ?);
        """, (new_subscription['author_id'],
              new_subscription['follower_id'],
              new_subscription['created_on'], ))
        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the comment dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_subscription['id'] = id


    return json.dumps(new_subscription)

def delete_subscription(id):
    """DOCSTRING
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Subscriptions
        WHERE id = ?
        """, (id, ))

def get_subscriptions_by_follower_id(follower_id):
    """gets all subscription posts"""
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT 
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
        FROM subscriptions s
        WHERE s.follower_id = ?
        """, ( follower_id, ))

        follower_subscriptions = []
        subscription_posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            subscription = Subscription(row['id'], row['follower_id'], row['author_id'],
                                        row['created_on'])

            subscription_author_id = subscription.author_id

            subscription_posts.append(get_post_by_user(subscription_author_id))

            subscription.post = subscription_posts

            follower_subscriptions.append(subscription.__dict__)

    return follower_subscriptions
