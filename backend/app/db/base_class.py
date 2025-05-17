"""
SQLAlchemy base class for all models.

This module provides the declarative base class for SQLAlchemy models
with common functionality for all models.

Requirements fulfilled:
- Common base class for all SQLAlchemy models
- Timestamp tracking
- Dictionary conversion
"""

import json
from datetime import datetime, date
from typing import Any, Dict

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import as_declarative, declared_attr


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that can handle dates and datetimes."""
    
    def default(self, obj: Any) -> Any:
        """
        Convert special types to JSON-serializable types.
        
        Args:
            obj: Object to serialize
            
        Returns:
            JSON-serializable value
        """
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


@as_declarative()
class Base:
    """
    Base class for all SQLAlchemy models.
    
    Provides common functionality like table name generation,
    conversion to dictionary, and attribute inspection.
    """
    # Generate __tablename__ automatically from class name
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name from class name.
        
        Returns:
            Lowercase table name
        """
        return cls.__name__.lower()
    
    def as_dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.
        
        Returns:
            Dictionary representation of the model
        """
        # Get all columns
        columns = inspect(self.__class__).columns.keys()
        
        # Convert each column value to a dict entry
        result = {}
        for column in columns:
            value = getattr(self, column)
            result[column] = value
        
        # Serialize dictionary to handle dates and other special types
        serialized = json.loads(
            json.dumps(result, cls=CustomJSONEncoder)
        )
        
        return serialized 