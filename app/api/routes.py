# app/api/routes.py
from flask import request, jsonify
from mongo_datatables import DataTables, Editor
from app import mongo
from app.api import api


@api.route('/mongo/<collection>', methods=['POST'])
def api_db(collection):
    data = {}
    try:
        data = request.get_json()
        field_types = {
            "Pages": "number",
            "Rating": "number",
            "PublishedDate": "date",
            "NovelId": "string",
            "Title": "string",
            "Author": "string",
            "Description": "string",
            "Themes": "array"
        }
        results = DataTables(mongo, collection, data, field_types=field_types).get_rows()
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
    data = {}
    try:
        data = request.get_json()
        doc_id = request.args.get('id', '')

        # Log the request details for debugging
        print(f"Editor request for {collection}:")
        print(f"Action: {data.get('action', 'unknown')}")
        print(f"Document ID: {doc_id}")
        print(f"Data keys: {list(data.keys())}")

        if data.get('action') == 'remove' and not doc_id:
            # Special handling for remove without ID
            print("ERROR: Remove operation without document ID")
            return jsonify({
                'error': 'Document ID is required for remove operation',
                'data': []
            }), 400

        # Process the request
        result = Editor(mongo, collection, data, doc_id).process()
        return jsonify(result)
    except Exception as e:
        # Log the error
        print(f"Editor error: {str(e)}")
        import traceback
        print(traceback.format_exc())

        # Return error response
        return jsonify({
            'error': str(e),
            'data': []
        }), 500
