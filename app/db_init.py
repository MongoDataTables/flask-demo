# db_init.py
from flask import current_app
from app.config import COLLECTION


def create_indexes():
    try:
        print("Creating Indexes")
        current_app.mongo.db[COLLECTION].create_index([
            ('Title', 'text'),
            ('Author', 'text'),
            ('Description', 'text')
        ])

        # Create regular indexes for sorting/filtering
        current_app.mongo.db[COLLECTION].create_index('Author')
        current_app.mongo.db[COLLECTION].create_index('Title')
        current_app.mongo.db[COLLECTION].create_index('Description')
        current_app.mongo.db[COLLECTION].create_index('Pages')
        current_app.mongo.db[COLLECTION].create_index('Rating')
        current_app.mongo.db[COLLECTION].create_index('PublishedDate')

        print("MongoDB indexes created successfully!")
    except Exception as e:
        print(f"Error creating indexes: {e}")
        import traceback
        print(traceback.format_exc())
