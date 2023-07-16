#!/usr/bin/python3
"""Unittest module for the FileStorage class."""

import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test cases for the FileStorage class"""

    def setUp(self):
        """Set up method executed before each test"""
        pass

    def tearDown(self):
        """Tear down method executed after each test"""
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        """Test if all() returns the correct objects dictionary"""
        # Test if all() returns an empty dictionary initially
        objects = storage.all()
        self.assertIsInstance(objects, dict)
        self.assertEqual(len(objects), 0)

        # Test if all() returns the correct dictionary after adding objects
        user = User()
        state = State()
        storage.new(user)
        storage.new(state)
        objects = storage.all()
        self.assertEqual(len(objects), 2)
        self.assertIn(f"{type(user).__name__}.{user.id}", objects)
        self.assertIn(f"{type(state).__name__}.{state.id}", objects)
        self.assertIs(objects[f"{type(user).__name__}.{user.id}"], user)
        self.assertIs(objects[f"{type(state).__name__}.{state.id}"], state)

    def test_new(self):
        """Test if new() adds the object to the objects dictionary"""
        user = User()
        state = State()
        storage.new(user)
        storage.new(state)
        objects = storage.all()
        self.assertEqual(len(objects), 2)
        self.assertIn(f"{type(user).__name__}.{user.id}", objects)
        self.assertIn(f"{type(state).__name__}.{state.id}", objects)
        self.assertIs(objects[f"{type(user).__name__}.{user.id}"], user)
        self.assertIs(objects[f"{type(state).__name__}.{state.id}"], state)

    def test_save_reload(self):
        """Test if save() serializes objects and reload(
        deserializes objects"""
        user = User()
        state = State()
        storage.new(user)
        storage.new(state)
        storage.save()
        storage.reload()
        objects = storage.all()
        self.assertEqual(len(objects), 2)
        self.assertIn(f"{type(user).__name__}.{user.id}", objects)
        self.assertIn(f"{type(state).__name__}.{state.id}", objects)
        self.assertIsInstance(objects[f"{type(user).__name__}.{user.id}"],
                              User)
        self.assertIsInstance(objects[f"{type(state).__name__}.{state.id}"],
                              State)

    def test_class_map(self):
        """Test if class_map property returns the correct class mapping"""
        class_map = storage.class_map
        self.assertIsInstance(class_map, dict)
        self.assertEqual(len(class_map), 7)
        self.assertIn("BaseModel", class_map)
        self.assertIn("User", class_map)
        self.assertIn("State", class_map)
        self.assertIn("City", class_map)
        self.assertIn("Amenity", class_map)
        self.assertIn("Place", class_map)
        self.assertIn("Review", class_map)
        self.assertIs(class_map["BaseModel"], BaseModel)
        self.assertIs(class_map["User"], User)
        self.assertIs(class_map["State"], State)
        self.assertIs(class_map["City"], City)
        self.assertIs(class_map["Amenity"], Amenity)
        self.assertIs(class_map["Place"], Place)
        self.assertIs(class_map["Review"], Review)

    def test_attributes(self):
        """Test if attributes() returns the valid attributes and their types"""
        attrs = storage.attributes()
        self.assertIsInstance(attrs, dict)
        self.assertEqual(len(attrs), 7)
        self.assertIn("BaseModel", attrs)
        self.assertIn("User", attrs)
        self.assertIn("State", attrs)
        self.assertIn("City", attrs)
        self.assertIn("Amenity", attrs)
        self.assertIn("Place", attrs)
        self.assertIn("Review", attrs)
        self.assertIsInstance(attrs["BaseModel"], dict)
        self.assertIsInstance(attrs["User"], dict)
        self.assertIsInstance(attrs["State"], dict)
        self.assertIsInstance(attrs["City"], dict)
        self.assertIsInstance(attrs["Amenity"], dict)
        self.assertIsInstance(attrs["Place"], dict)
        self.assertIsInstance(attrs["Review"], dict)
        # Test a few specific attributes and their types
        self.assertIn("id", attrs["BaseModel"])
        self.assertIs(attrs["BaseModel"]["id"], str)
        self.assertIn("email", attrs["User"])
        self.assertIs(attrs["User"]["email"], str)
        self.assertIn("name", attrs["State"])
        self.assertIs(attrs["State"]["name"], str)
        self.assertIn("latitude", attrs["Place"])
        self.assertIs(attrs["Place"]["latitude"], float)
        self.assertIn("text", attrs["Review"])
        self.assertIs(attrs["Review"]["text"], str)


if __name__ == '__main__':
    unittest.main()
