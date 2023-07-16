#!/usr/bin/python3
"""unittest for State class"""

import os
import unittest
from models import storage
from models.state import State
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestState(unittest.TestCase):
    """State class test cases"""

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

    def test_8_instantiation(self):
        """instantiation tests"""
        obj = State()
        self.assertEqual(str(type(obj)), "<class 'models.state.State'>")
        self.assertIsInstance(obj, State)
        self.assertTrue(issubclass(type(obj), BaseModel))

    def test_8_attrs(self):
        """Attributes tests"""
        attributes = storage.attributes()["State"]
        obj = State()
        for k, v in attributes.items():
            self.assertTrue(hasattr(obj, k))
            self.assertEqual(type(getattr(obj, k, None)), v)


if __name__ == "__main__":
    unittest.main()
