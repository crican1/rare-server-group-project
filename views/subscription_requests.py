import sqlite3
import json
from models import Subscription

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

def create_subscription(subscription):
    """DOCSTRING
    """
    # Get the id value of the last animal in the list
    max_id = SUBSCRIPTIONS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    subscription["id"] = new_id

    # Add the animal dictionary to the list
    SUBSCRIPTIONS.append(subscription)

    # Return the dictionary with `id` property added
    return subscription

def delete_subscription(id):
    """DOCSTRING
    """
    # Initial -1 value for animal index, in case one isn't found
    subscription_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, subscription in enumerate(SUBSCRIPTIONS):
        if subscription["id"] == id:
            # Found the animal. Store the current index.
            subscription_index = index

    # If the animal was found, use pop(int) to remove it from list
    if subscription_index >= 0:
        SUBSCRIPTIONS.pop(subscription_index)
