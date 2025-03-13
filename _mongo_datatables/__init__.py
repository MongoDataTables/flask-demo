"""
MongoDB integration with jQuery DataTables
"""
__version__ = '1.0.0'

from _mongo_datatables.datatables import DataTables
from _mongo_datatables.editor import Editor

__all__ = ['DataTables', 'Editor']