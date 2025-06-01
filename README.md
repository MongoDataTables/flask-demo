# MongoDB DataTables Flask Demo

A demonstration application showcasing the integration of MongoDB with jQuery DataTables for efficient server-side processing, built using Flask 3.x.

## About This Project

This demo application illustrates how to use the `mongo-datatables` Python package to connect MongoDB collections with DataTables, enabling powerful server-side processing for large datasets with minimal configuration.

The demo presents a fictional "Dystopian Archives" database to showcase various features including:

- Server-side pagination, sorting, and filtering
- Global search across multiple fields
- Column-specific searches
- Support for nested document structures
- Type-aware search operations (dates, numbers, text, etc.)
- Proper handling of MongoDB data types

## Prerequisites

- Python 3.9.6+
- MongoDB 5.0+ (running locally or accessible via network)
- pip (Python package manager)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/MongoDataTables/flask-demo.git
   cd flask-demo
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. **Important:** DataTables Editor is a commercial product and is not included in this repository.
   - If you wish to enable the editing features, purchase a license from [DataTables Editor](https://editor.datatables.net/)
   - Download and place the Editor files in `app/static/Editor-2.4.1/`
   - Uncomment the Editor-related lines in the HTML templates

## Seeding Data

To test and demonstrate the functionality of this application, you'll need sample data in your MongoDB database. The project includes a data seeding script that generates sample book records with dystopian themes.

### Basic Usage

```bash
# Install required packages
pip install pymongo faker

# Generate 100 sample books (default)
python seed_data.py

# Generate a specific number of books
python seed_data.py --count 1000

# Generate books with larger batch size (for better performance)
python seed_data.py --count 10000 --batch-size 5000

# Use a custom MongoDB connection string
python seed_data.py --connection "mongodb://username:password@hostname:port/"
```

### Data Structure

The seeding script creates book records with the following structure:

```javascript
{
  "NovelId": "DYST-1A2B3C4D",       // Unique identifier
  "Title": "The Last Horizon",       // Book title
  "Author": "Alex Zhang",            // Author name
  "PublisherInfo": {                 // Nested publisher information
    "Name": "Dystopian Press",
    "Date": ISODate("2022-03-15"),
    "Location": "New York",
    "Edition": 2,
    "Details": {
      "ISBN": "978-1234567890",
      "Format": "Hardcover",
      "PrintRun": 25000
    }
  },
  "Pages": 324,                      // Page count
  "Themes": [                        // Array of themes
    "Environmental collapse", 
    "Post-apocalyptic survival"
  ],
  "Rating": 4.5,                     // Book rating
  "Description": "A haunting exploration of environmental collapse..."
}
```

This structure demonstrates many MongoDB capabilities including nested documents and arrays, making it perfect for testing the DataTables and Editor integration.

## Enabling DataTables Editor

This demo application is designed to work with or without the DataTables Editor component, which is a paid jQuery library for adding editing capabilities to DataTables.

To enable Editor functionality:

1. Purchase a license from [DataTables Editor](https://editor.datatables.net/)
2. Download the Editor files and place them in the following directory structure:
   ```
   app/static/Editor-2.4.1/
   ├── css/
   │   └── editor.bootstrap5.min.css
   └── js/
       ├── dataTables.editor.min.js
       └── editor.bootstrap5.min.js
   ```
3. Uncomment the Editor-related lines in `app/templates/books.html`:
   ```html
   <!-- DataTables Editor CSS - Uncomment to enable editing functionality -->
   <link href="{{ url_for('static', filename='Editor-2.4.1/css/editor.bootstrap5.min.css') }}" rel="stylesheet">
   
   <!-- DataTables Editor JS - Uncomment to enable editing functionality -->
   <script src="{{ url_for('static', filename='Editor-2.4.1/js/dataTables.editor.min.js') }}"></script>
   <script src="{{ url_for('static', filename='Editor-2.4.1/js/editor.bootstrap5.min.js') }}"></script>
   ```

The application will automatically detect the presence of the Editor library and enable the editing functionality accordingly. If Editor is not available, the application will display a read-only view with export buttons instead of edit buttons.

### Scaling to Millions of Records

The seeding script supports generating millions of records for performance testing. When generating large datasets:

1. Consider increasing the batch size (for faster insertion)
2. Ensure your MongoDB instance has sufficient storage space
3. Be patient - generating 20M records will take time but the script provides progress updates

```bash
# Generate 2 million records (this will take a while)
python seed_data.py --count 2000000 --batch-size 1000
```

Remember it's important to create appropriate indexes on your MongoDB collection after seeding to ensure good query performance. The `tools/db_init.py` script will run on start-up if you forget.

## Configuration

1. Update the MongoDB connection settings in `app/config.py` if needed:
   ```python
   MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/book_database")
   ```

2. Initialize the database with sample dat manually (or the script will run on start-up):
   ```
   python -m app.tools.db_init
   ```

## Running the Application

Start the development server:
```
cd app
flask run
```

The application will be available at [http://localhost:5000](http://localhost:5000)

## Project Structure

```
flask-demo/
├── app/                      # Main application package
│   ├── books/                # Books blueprint (combined API and views)
│   │   ├── __init__.py       # Blueprint initialization
│   │   └── routes.py         # All routes including API endpoints
│   ├── static/               # Static files (CSS, JS, etc.)
│   │   ├── css/              # Custom CSS
│   │   ├── js/               # JavaScript files
│   │   └── favicon/          # Favicon files
│   ├── templates/            # Jinja2 templates
│   │   └── books.html        # Combined template for the application
│   ├── tools/                # Utility scripts
│   │   └── db_init.py        # Database initialization
│   ├── __init__.py           # Application factory
│   ├── app.py                # Application entry point
│   └── config.py             # Configuration settings
├── docs/                     # Documentation
├── seed_data.py              # Script to generate sample data
└── requirements.txt          # Python dependencies
```

## Features Demonstrated

### Server-Side Processing
The demo shows how to handle large datasets efficiently by processing them on the server side, sending only the data that needs to be displayed to the client.

### Advanced Search
- Global search across all visible columns
- Column-specific search filters
- Special syntax for field-specific searches (`field:value`)
- Type-aware searching for dates, numbers, and text

### MongoDB Integration
- Efficient aggregation pipelines
- Proper handling of MongoDB data types
- Support for nested document fields using dot notation
- Text index utilization when available

### DataTables Editor Integration
For users with a DataTables Editor license, the demo includes:
- Create, edit, and delete operations
- Field validation
- Proper handling of complex data types

## External Libraries

Most JavaScript and CSS resources are loaded from CDNs for simplicity:
- DataTables 2.2.2
- Bootstrap 5.3.2
- jQuery 3.7.1
- Various DataTables extensions

## License

This demo is released under the MIT License. See the LICENSE file for details.

The `mongo-datatables` package is also available under the MIT License.

## Note on DataTables Editor

This demo supports DataTables Editor integration, but Editor is a commercial product and must be purchased separately from [https://editor.datatables.net/](https://editor.datatables.net/). Once purchased, place the files in the `app/static/Editor-2.4.1/` directory and uncomment the relevant sections in the templates.

## Related Projects

- [mongo-datatables](https://github.com/MongoDataTables/mongo-datatables) - The core Python package used in this demo
- [Django Demo](https://github.com/MongoDataTables/django-demo) - Similar demo using Django instead of Flask

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
