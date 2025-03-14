# tools/db_init.py
from flask import current_app


def create_indexes():
    try:
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
