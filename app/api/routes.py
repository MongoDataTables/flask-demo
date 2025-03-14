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

        # Enhanced debugging for the editor request
        print(f"\n==== Editor request for {collection} ====")
        print(f"Action: {data.get('action', 'unknown')}")
        print(f"Document ID: {doc_id}")

        # For edit actions, print the actual data values and types for Rating
        if data.get('action') == 'edit' and collection == 'books':
            for id_key, doc_data in data.get('data', {}).items():
                if 'Rating' in doc_data:
                    rating_value = doc_data['Rating']
                    print(f"Rating value in request: {rating_value} (type: {type(rating_value).__name__})")

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

        # Create a subclass of Editor to add debugging
        class DebugEditor(Editor):
            def _process_updates(self, data, updates, prefix=""):
                """Override to add debugging for Rating values"""
                super()._process_updates(data, updates, prefix)

                # After processing, check for Rating field in updates
                for key, value in updates.items():
                    if key == 'Rating':
                        print(f"Rating after processing: {value} (type: {type(value).__name__})")

            def edit(self):
                """Override to add debugging before MongoDB update"""
                result = super().edit()

                # Look for Rating in the result data
                if 'data' in result:
                    for doc in result.get('data', []):
                        if 'Rating' in doc:
                            print(f"Rating in response: {doc['Rating']} (type: {type(doc['Rating']).__name__})")

                return result

        result = DebugEditor(mongo, collection, data, doc_id, field_types=field_types).process()

        # Debug the final result
        if collection == 'books' and 'data' in result:
            for doc in result.get('data', []):
                if 'Rating' in doc:
                    print(f"Final Rating in response: {doc['Rating']} (type: {type(doc['Rating']).__name__})")

        return jsonify(result)

    except Exception as e:
        print(f"Editor error: {str(e)}")
        import traceback
        print(traceback.format_exc())

        # Return error response
        return jsonify({
            'error': str(e),
            'data': []
        }), 500
