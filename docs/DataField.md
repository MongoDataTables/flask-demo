# Using DataField in mongo-datatables

## Overview

The `DataField` class provides a powerful way to define and manage your MongoDB fields when using mongo-datatables. While not strictly required for basic functionality, it offers significant advantages for complex data structures, type handling, and UI integration.

## Basic Usage

```python
from mongo_datatables import DataTables, DataField

# Define your data fields
fields = [
    DataField("Title", "string"),
    DataField("Author", "string"),
    DataField("PublisherInfo.Date", "date", alias="Published"),
    DataField("Pages", "number")
]

# Create DataTables instance with these fields
dt = DataTables(mongo, "books", request.get_json(), data_fields=fields)
```

## Why Use DataField?

### 1. Type-Aware Operations

DataField ensures that each field's data type is properly handled during:
- Searching (e.g., date ranges vs. text searches)
- Sorting (e.g., numeric vs. lexicographic ordering)
- Filtering (e.g., applying appropriate operators)

```python
# Date fields will be properly parsed and compared
DataField("PublisherInfo.Date", "date")

# Numeric fields will use numeric comparisons
DataField("Pages", "number")
```

### 2. UI/Database Field Mapping

Map user-friendly field names in your UI to actual database field paths:

```python
# In the UI, this appears as "Published"
# In the database, it's stored as "PublisherInfo.Date"
DataField("PublisherInfo.Date", "date", alias="Published")
```

### 3. Nested Field Support

Easily work with nested document structures:

```python
# Access nested fields with dot notation
DataField("Publisher.Name", "string")
DataField("Publisher.Location.City", "string", alias="City")
```

### 4. Validation

DataField validates field types against MongoDB's supported types:
```
string, number, date, boolean, array, object, objectId, null
```

## Legacy Support

For backward compatibility, mongo-datatables still supports the older approach using a simple dictionary:

```python
# Legacy approach (not recommended for new code)
field_types = {
    "Title": "string",
    "Pages": "number"
}

dt = DataTables(mongo, "books", request.get_json(), field_types=field_types)
```

However, this approach lacks the benefits of field validation, UI mapping, and explicit nested field support.

## Best Practices

1. Always define `DataField` objects for all queryable fields
2. Use appropriate data types to ensure optimal query performance
3. Provide user-friendly aliases for complex field paths
4. For nested fields, always use the full path with dot notation

By leveraging the `DataField` class, you'll create more maintainable, type-safe, and user-friendly applications with mongo-datatables.
