# app/tools/db_init.py
from flask import current_app
from pymongo import MongoClient


def create_indexes(db=None):
    try:
        # Use the provided db or get it from Flask's current_app
        if db is None:
            db = current_app.mongo.db  # type: ignore

        print("Creating Indexes")
        # Create text indexes for full-text search capabilities
        db["books"].create_index([
            ('Title', 'text'),
            ('Author', 'text'),
            ('Description', 'text'),
            ('Themes', 'text')  # Added Themes array for text search
        ])

        # Create regular indexes for sorting/filtering
        # Basic fields
        db["books"].create_index('NovelId')
        db["books"].create_index('Title')
        db["books"].create_index('Author')
        db["books"].create_index('Pages')
        db["books"].create_index('Rating')
        db["books"].create_index('Description')
        db["books"].create_index('Themes')

        # Nested fields
        db["books"].create_index('PublisherInfo.Date')  # Important for date filtering

        print("MongoDB indexes created successfully!")

        # Print field_types information for reference
        print("\nRecommended field_types configuration:")
        print("""
field_types = {
    "Title": "text",
    "Author": "text",
    "PublisherInfo.Date": "date",
    "PublisherInfo.Edition": "number",
    "Themes": "array",
    "Pages": "number",
    "Rating": "number"
}
        """)

    except Exception as e:
        print(f"Error creating indexes: {e}")
        import traceback
        print(traceback.format_exc())


def main():
    """Run as standalone script"""
    import argparse

    parser = argparse.ArgumentParser(description='Create MongoDB indexes for book database')
    parser.add_argument('--uri', type=str, default='mongodb://localhost:27017/book_database',
                        help='MongoDB connection string (default: mongodb://localhost:27017/book_database)')

    args = parser.parse_args()

    # Connect directly to MongoDB
    client = MongoClient(args.uri)
    db = client.get_database()

    print(f"Connected to MongoDB: {args.uri}")
    create_indexes(db)


if __name__ == "__main__":
    # This will be executed when running as python -m app.tools.db_init
    main()
