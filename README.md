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
   cd mongo-datatables-flask-demo
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
python seed_books.py

# Generate a specific number of books
python seed_books.py --count 1000

# Generate books with larger batch size (for better performance)
python seed_books.py --count 10000 --batch-size 5000

# Use a custom MongoDB connection string
python seed_books.py --connection "mongodb://username:password@hostname:port/"
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

### Scaling to Millions of Records

The seeding script supports generating millions of records for performance testing. When generating large datasets:

1. Consider increasing the batch size (for faster insertion)
2. Ensure your MongoDB instance has sufficient storage space
3. Be patient - generating 20M records will take time but the script provides progress updates

```bash
# Generate 20 million records (this will take a while)
python seed_books.py --count 20000000 --batch-size 10000
```

Remember to create appropriate indexes on your MongoDB collection after seeding to ensure good query performance.

## Configuration

1. Update the MongoDB connection settings in `app/config.py` if needed:
   ```python
   MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/book_database")
   ```

2. Initialize the database with sample data:
   ```
   python -m app.tools.db_init
   ```

## Running the Application

Start the development server:
```
python app/app.py
```

The application will be available at [http://localhost:5000](http://localhost:5000)

## Project Structure

```
mongo-datatables-flask-demo/
├── app/                      # Main application package
│   ├── api/                  # API blueprint
│   │   ├── __init__.py       # Blueprint initialization
│   │   └── routes.py         # API endpoints
│   ├── main/                 # Main blueprint
│   │   ├── __init__.py       # Blueprint initialization
│   │   └── routes.py         # View functions
│   ├── static/               # Static files (CSS, JS, etc.)
│   │   ├── css/              # Custom CSS
│   │   └── favicon/          # Favicon files
│   ├── templates/            # Jinja2 templates
│   ├── tools/                # Utility scripts
│   │   └── db_init.py        # Database initialization
│   ├── __init__.py           # Application factory
│   ├── app.py                # Application entry point
│   └── config.py             # Configuration settings
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

## API Documentation

The demo exposes the following API endpoints:

### `/api/books` (POST)
Main endpoint for DataTables server-side processing.

**Request:**
- DataTables request format with draw, start, length, etc.

**Response:**
```json
{
  "draw": 1,
  "recordsTotal": 100,
  "recordsFiltered": 20,
  "data": [
    {
      "Title": "1984",
      "Author": "George Orwell",
      "PublisherInfo": {"Date": "1949-06-08", "Edition": 1},
      "DT_RowId": "60f1a5b3e4b0a1b2c3d4e5f6"
    },
    ...
  ]
}
```

### `/api/editor/<collection>` (POST)
For DataTables Editor operations (create, edit, remove).

## Handling Numeric Values in DataTables with MongoDB

When working with numeric values in DataTables and MongoDB, there are important considerations regarding how numbers are processed between JavaScript, Python, and MongoDB.

### The Issue: Floating Point Numbers with Zero Decimal Places

JavaScript doesn't distinguish between integers and floating-point numbers when the decimal part is zero. If you define a value as `5.0` in JavaScript, it's treated internally as just `5` (an integer).

This can cause inconsistencies when:
1. You want to display numeric values consistently with decimal places (e.g., always showing "5.0" instead of "5")
2. You need to preserve the exact numeric type (float vs. integer) in your database

### How DataTables Processes Numeric Values

When you define select options in DataTables Editor:

```javascript
options: [
    { label: "★★½ (2.5)", value: 2.5 },
    { label: "★★★ (3.0)", value: 3.0 },
    { label: "★★★★★ (5.0)", value: 5.0 }
]
```

Here's what happens:
1. For values with non-zero decimal parts (like 2.5), JavaScript maintains them as floating-point
2. For values with zero decimal parts (like 3.0 or 5.0), JavaScript converts them to integers (3 or 5)
3. When sending to the server, they're sent as numeric JSON values, not strings

### Solutions for Consistent Numeric Handling

#### Option 1: Force values to be strings in DataTables (Recommended)

This approach ensures consistent handling by always sending strings to the server:

```javascript
options: [
    { label: "★★½ (2.5)", value: "2.5" },
    { label: "★★★ (3.0)", value: "3.0" },
    { label: "★★★★★ (5.0)", value: "5.0" }
]
```

**Advantages:**
- Strings are processed through the string-to-number conversion in the Editor class
- Values with decimal points are properly recognized as floats
- The display format is preserved

#### Option 2: Format Display Values in the Table

If you only care about consistent display but not storage type:

```javascript
{
    data: 'Rating',
    render: function(data) {
        return parseFloat(data).toFixed(1);  // Always display with one decimal place
    }
}
```

### When to Use Each Approach

1. **Use Option 1 (string values)** when:
   - You want consistent handling of float vs. integer without modifying your backend
   - You need to preserve the decimal format for storage and display
   - You want the actual stored value to maintain its decimal precision

2. **Use Option 2 (display formatting)** when:
   - You only care about display consistency
   - The actual storage format (int vs. float) doesn't matter
   - You prefer working with native JavaScript numeric values in your code

### MongoDB Number Storage Behavior

MongoDB internally optimizes numeric storage:
- Integers are stored as 32-bit or 64-bit integers
- Decimals with zero fractional parts (`5.0`) are typically stored as integers (`5`)

This is normal behavior and usually doesn't affect functionality, but it can impact how numbers are returned and displayed if you rely on type exactness.

### Best Practice Recommendation

For consistent handling of numeric values with decimal places, use **Option 1** and define Editor values as strings. This provides the cleanest solution with the least chance of inconsistency across the JavaScript-Python-MongoDB pipeline.

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

