# Python Descriptor

This project demonstrates the practical use of Python descriptors through a User Profile Management system. It showcases how descriptors can be used for data validation, caching, and property management.



## What are Descriptors?

Descriptors are Python objects that define how attribute access is intercepted. They implement at least one of the descriptor protocol methods:
- `__get__(self, obj, owner=None)`
- `__set__(self, obj, value)`
- `__delete__(self, obj)`

Descriptors provide a powerful way to customize attribute access and are the mechanism behind many Python features like properties, methods, and class methods.


There are two types of descriptors:
- Data descriptors: Implement both `__get__` and `__set__`
- Non-data descriptors: Implement only `__get__`



## Implementation Details

### ValidatedProperty Descriptor

In  `user_profile_manager.py`,  implementation of a custom descriptor called `ValidatedProperty` that handles:

1. **Validation**: Validates data before assignment using customizable validator functions

Each property has its own validation rules:
- `username`: Must be a non-empty string
- `email`: Must be a string containing '@' and '.'
- `last_login`: Must be either None or a datetime object

### Features

1. **Type Safety**
   - Strong type checking through validators
   - Type hints for better IDE support
   - Clear error messages for invalid values

2. **Memory Management**
   - Weak references prevent memory leaks
   - Automatic cleanup of unused instances
   - Efficient caching system

3. **Default Values**
   - Class-level defaults for properties
   - Special handling for nullable fields
   - Consistent property resolution

## Example Usage

```python
#  Create a new user profile
profile = UserProfileManager()

# Set valid values
profile.username = "john_doe" # Valid
profile.email = "john@example.com" # Valid
profile.last_login = datetime.now() # Valid

# These will raise ValueError:
profile.username = "" # Invalid: empty string
profile.email = "invalid_email" # Invalid: missing @ and .
profile.last_login = "not_a_datetime" # Invalid: wrong type
```

This implementation ensures that only valid data is accepted, providing a robust and type-safe way to manage user profiles.

## Testing

The project includes comprehensive tests that verify:
- Property validation
- Caching behavior
- Default value handling
- Memory management
- Edge cases

Run tests using pytest:
```bash
pytest -vsk .
```

This ensures that the descriptor implementation is robust and handles all specified cases correctly.

## Links

- [Descriptor Concept](https://www.youtube.com/watch?v=ZdvpNaWwx24&ab_channel=InfoQ)
- [Descriptor Example](https://www.youtube.com/watch?v=mMbVs17Vmo4&ab_channel=mCoding)