import json
from flask import render_template, request, jsonify
from mongo_datatables import DataTables, Editor, DataField
from app import mongo
from app.books import books

# Define common data fields for the books collection
BOOKS_DATA_FIELDS = [
    DataField("Title", "string"),
    DataField("Author", "string"),
    DataField("PublisherInfo.Date", "date", alias="Published"),  # Nested field with UI alias
    DataField("Themes", "array"),
    DataField("Pages", "number"),
    DataField("Rating", "number")
]


# Main routes
@books.route('/')
@books.route('/index')
def index():
    return render_template('books.html')


# API routes
@books.route('/api/books', methods=['POST'])
def books_data():
    """Endpoint specifically for the books collection demo."""
    data = {}
    try:
        data = request.get_json()
        dt = DataTables(mongo, "books", data, data_fields=BOOKS_DATA_FIELDS, debug_mode=False)
        results = dt.get_rows()
        return jsonify(results)
    except Exception as e:
        import traceback
        print(f"ERROR in books_data: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'data': [],
            'draw': data.get('draw', 1),
            'recordsTotal': 0,
            'recordsFiltered': 0
        }), 500


@books.route('/api/editor/books', methods=['POST'])
def api_editor():
    try:
        data = request.get_json()
        doc_id = request.args.get('id', '')
        data_fields = BOOKS_DATA_FIELDS  # Use data_fields for large collections or nested fields
        result = Editor(mongo, "books", data, doc_id, data_fields=data_fields).process()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'data': []
        }), 500
