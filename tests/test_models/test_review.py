#!/usr/bin/python3
"""unittest for Review  class"""

import os
import unittest
from models import storage
from models.review import Review
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestReview(unittest.TestCase):
    """Review class test cases"""

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
        obj = Review()
        self.assertEqual(str(type(obj)), "<class 'models.review.Review'>")
        self.assertIsInstance(obj, Review)
        self.assertTrue(issubclass(type(obj), BaseModel))

    def test_8_attrs(self):
        """Attributes tests"""
        attributes = storage.attributes()["Review"]
        obj = Review()
        for k, v in attributes.items():
            self.assertTrue(hasattr(obj, k))
            self.assertEqual(type(getattr(obj, k, None)), v)


if __name__ == "__main__":
    unittest.main()
