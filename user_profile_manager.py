"""
UserProfileManager system that manages user profiles with validation and caching.

This module implements a user profile management system with the following features:
- Validated properties for username, email, and last_login
- Weak reference caching to prevent memory leaks
- Class-level defaults for unset properties
"""

# Standard Library Imports
import weakref
from datetime import datetime
from typing import Optional, Any, Callable


# ------------------------- ValidatedProperty Descriptor -------------------------
class ValidatedProperty:
    """
    A descriptor that validates data before assignment using a provided validation function.
    
    Attributes:
        validator (callable): Function to validate values before assignment
        values (WeakKeyDictionary): Storage for instance values using weak references
        name (str): Name of the property, set automatically via __set_name__
    """
    def __init__(self, validator: Optional[Callable[[Any, str], None]] = None) -> None:
        """
        Initialize the ValidatedProperty descriptor.

        Args:
            validator: Function that validates values before assignment.
                Should take (value, name) as parameters and raise ValueError if invalid.
        """
        self.validator = validator
        # Using WeakKeyDictionary to allow instance garbage collection
        self.values = weakref.WeakKeyDictionary()
    
    def __set_name__(self, owner: type, name: str) -> None:
        """
        Automatically bind the property name when the class is created.
        
        Args:
            owner: The class that owns this descriptor
            name: The name of this property in the owner class
        """
        self.name = name
        
    def __get__(self, instance: Optional[Any], owner_class: type) -> Any:
        """
        Get the property value for an instance.
        
        Args:
            instance: The instance accessing the property (None if accessed from class)
            owner_class: The class that owns this descriptor
        
        Returns:
            - The descriptor if accessed from the class
            - The default_last_login if property is last_login and no value is set
            - The instance's value if set
            - None otherwise
        """
        if instance is None:
            return self
            
        # Special handling for last_login to use class default
        if self.name == 'last_login' and instance not in self.values:
            return owner_class.default_last_login
        return self.values.get(instance)
        
    def __set__(self, instance: Any, value: Any) -> None:
        """
        Set the property value after validation.
        
        Args:
            instance: The instance being modified
            value: The value to set
            
        Raises:
            ValueError: If the validator rejects the value
        """
      #   print(f"Setting {self.name} to {value}")
        if self.validator:
            self.validator(value, self.name)
        self.values[instance] = value


def validate_username(value: Any, name: str) -> None:
    """
    Ensure username is a non-empty string.
    
    Args:
        value: The value to validate
        name: Name of the property being validated
        
    Raises:
        ValueError: If value is not a non-empty string
    """
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")


def validate_email(value: Any, name: str) -> None:
    """
    Ensure email is a string containing '@' and '.'.
    
    Args:
        value: The value to validate
        name: Name of the property being validated
        
    Raises:
        ValueError: If value is not a valid email string
    """
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    if '@' not in value or '.' not in value:
        raise ValueError(f"{name} must contain '@' and '.'")


def validate_last_login(value: Any, name: str) -> None:
    """
    Ensure last_login is either None or a datetime object.
    
    Args:
        value: The value to validate
        name: Name of the property being validated
        
    Raises:
        ValueError: If value is neither None nor a datetime object
    """
    if value is not None and not isinstance(value, datetime):
        raise ValueError(f"{name} must be a datetime object or None")


# ------------------------- UserProfileManager Class -------------------------
class UserProfileManager:
    """
    Manages user profiles with validation and caching.
    
    Features:
    - Validated username and email properties
    - Nullable last_login timestamp
    - Weak reference caching system
    - Class-level defaults for unset properties
    
    Attributes:
        username (str): The user's username (non-empty string)
        email (str): The user's email address (must contain @ and .)
        last_login (Optional[datetime]): Timestamp of last login
    """
    
    # Class-level cache using weak references for automatic cleanup
    _cache: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
    
    # Class-level default for last_login
    default_last_login: Optional[datetime] = None
    
    # Validated properties
    username = ValidatedProperty(validate_username)
    email = ValidatedProperty(validate_email) 
    last_login = ValidatedProperty(validate_last_login)

    @classmethod
    def add_to_cache(cls, instance: 'UserProfileManager') -> None:
        """
        Add a profile instance to the cache.
        
        Args:
            instance: UserProfileManager instance to cache
        """
        cls._cache[id(instance)] = instance
        
    @classmethod
    def get_from_cache(cls, instance_id: int) -> Optional['UserProfileManager']:
        """
        Retrieve a profile from the cache by ID.
        
        Args:
            instance_id: ID of the instance to retrieve
            
        Returns:
            The cached instance or None if not found
        """
        return cls._cache.get(instance_id)
    