# app/api/routes.py
from flask import request, jsonify
from mongo_datatables import DataTables, Editor
from app import mongo
from app.api import api


@api.route('/books', methods=['POST'])
def books_data():
    """Endpoint specifically for the books collection demo."""
    data = {}
    try:
        data = request.get_json()
        field_types = {
            "Title": "text",
            "Author": "text",
            "PublisherInfo.Date": "date",
            "Themes": "array",
            "Pages": "number",
            "Rating": "number",
        }
        results = DataTables(mongo, 'books', data, field_types=field_types).get_rows()
        return jsonify(results)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'data': [],
            'draw': data.get('draw', 1),
            'recordsTotal': 0,
            'recordsFiltered': 0
        }), 500


@api.route('/editor/<collection>', methods=['POST'])
def api_editor(collection):
    try:
        data = request.get_json()
        doc_id = request.args.get('id', '')

        # Define field_types based on collection
        field_types = {}
        if collection == 'books':
            field_types = {
                "Title": "text",
                "Author": "text",
                "PublisherInfo.Date": "date",
                "PublisherInfo.Edition": "number",
                "Themes": "array",
                "Pages": "number",
                "Rating": "number",
                "Description": "text"
            }

        result = Editor(mongo, collection, data, doc_id, field_types=field_types).process()
        return jsonify(result)

    except Exception as e:
        # Return error response
        return jsonify({
            'error': str(e),
            'data': []
        }), 500
