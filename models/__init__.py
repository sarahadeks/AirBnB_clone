#!/usr/bin/python3
"""create a unique FileStorage instance for your application.
Placing this code in the __init__.py file allows you to initialize the
storage and load the data automatically whenever you import or use the
package or module. This ensures that the data is available for use without
explicitly calling the initialization and reload steps in every module
that requires the serialized data."""
from models.engine.file_storage import FileStorage

# The purpose of this code is to set up the storage mechanism
# and load any previously serialized data from the file
storage = FileStorage()
storage.reload()
