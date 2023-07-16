#!/usr/bin/python3
"""unittest for Amentity class"""

import os
import unittest
from models import storage
from models.place import Place
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestPlace(unittest.TestCase):
    """Place class test cases"""

    def setUP(self):
        """SetUp"""
        pass

    def tearDown(self):
        """Tear Down"""
        self.reset_storage()
        pass

    def reset_storage(self):
        """Reset storage"""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_instantiation(self):
        """instantiation tests"""
        obj = Place()
        self.assertEqual(str(type(obj)), "<class 'models.place.Place'>")
        self.assertIsInstance(obj, Place)
        self.assertTrue(issubclass(type(obj), BaseModel))

    def test_attrs(self):
        """Attributes tests"""
        attributes = storage.attributes()["Place"]
        obj = Place()
        for k, v in attributes.items():
            self.assertTrue(hasattr(obj, k))
            self.assertEqual(type(getattr(obj, k, None)), v)


if __name__ == "__main__":
    unittest.main()
