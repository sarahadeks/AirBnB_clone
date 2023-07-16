#!/usr/bin/python3
"""Test for storage"""
import unittest
from models.engine.file_storage import FileStorage


class test_fileStorage(unittest.TestCase):
    """Test FileStorage Class"""
    def test_instances(self):
        """test instances"""
        obj = FileStorage()
        self.assertIsInstance(obj, FileStorage)

    def test_methods(self):
        """test methods not  none"""
        self.assertIsNotNone(FileStorage.all)
        self.assertIsNotNone(FileStorage.new)
        self.assertIsNotNone(FileStorage.save)
        self.assertIsNotNone(FileStorage.reload)


if __name__ == '__main__':
    unittest.main()
