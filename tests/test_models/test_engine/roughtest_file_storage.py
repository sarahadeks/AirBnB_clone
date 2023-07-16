#!/usr/bin/python3
"""Unittest for FileStorage Class"""
import os
import re
import time
import json
import uuid
import unittest
from models import storage
from datetime import datetime
from models.base_model import FileStorage
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage class"""

    def setUp(self):
        """Setup"""
        pass

    def tearDown(self):
        """Teardown"""
        self.reset_storage()
        pass

    def reset_storage(self):
        """Resets the storage data"""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_instantiation(self):
        """Test instantiation"""
        self.assertEqual((type(storage).__name__, "FileStorage")

    def test_init_no_args(self):
        """Testing __init__ with no arguments."""
        self.reset_storage()
        with self.assertRaises(TypeError) as e:
            FileStorage.__init__()
        msg = "descriptor '__init__' of 'object' object needs an argument"
        self.assertEqual(str(e.exception), msg)

    def test_init_with_many_args(self):
        """Testing __init__ with many arguments."""
        self.reset_storage()
        with self.assertRaises(TypError) as e:
            obj = FileStorage(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        message = "object() takes no parameters"
        self.asserEqual(str(e.exception), message)

    def test_attributes(self):
        """Tests for attributes of FileStorage"""
        self.reset_storage()
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertEqual(getattr(FileStorage, "_FileStorage__objects", {}))

    def test_id(self):
        """Tests for unique ids."""
        uniq_ids = [FileStorage().id for i in range(1000)]
        self.assertEqual(len(set(uniq_ids)), len(uniq_ids))

    def test_datetime_created_at_updaed_at(self):
        """Testing difference btw  updated_at & created_at to make sure
        the current at creation"""
        date_now = datetime.now()
        obj = FileStorage()
        diff = obj.updated_at - obj.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        diff = obj.created_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.1)

    def test_save(self):
        """Tests save()"""
        obj = FileStorage()
        time.sleep(0.5)
        datenow = datetime.now()
        obj.save()
        diff = obj.updated_at - datenow
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_str(self):
        """Tests  __str__()"""
        obj = FileStorage()
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(str(obj))
        self.assertIsNotNone(res)
        self.assertEqual(res.group(1), "FileStorage")
        self.assertEqual(res.group(2), obj.id)
        s = res.group(3)
        s = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s)
        d = json.loads(s.replace("'", '"'))
        d2 = obj.__dict__.copy()
        d2["created_at"] = repr(d2["created_at"])
        d2["updated_at"] = repr(d2["updated_at"])
        self.assertEqual(d, d2)

    def test_to_dict(self):
        """Tests to_dict()"""
        obj = FileStorage()
        obj.name = "John"
        obj.age = 34
        d = obj.to_dict()
        self.assertEqual(d["id"], obj.id)
        self.assertEqual(d["__class__"], type(obj).__name__)
        self.assertEqual(d["created_at"], obj.created_at.isoformat())
        self.assertEqual(d["updated_at"], obj.updated_at.isoformat())
        self.assertEqual(d["name"], obj.name)
        self.assertEqual(d["age"], obj.age)

    def test_to_dict_with_many_args(self):
        """Tests to_dict() with too many arguments."""
        self.reset_storage()
        with self.assertRaises(TypeError) as e:
            FileStorage.to_dict(self, 98)
        msg = "to_dict() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), msg)

    def test_to_dict_with_no_args(self):
        """Tests to_dict() with no arguments."""
        self.reset_storage()
        with self.assertRaises(TypeError) as e:
            FileStorage.to_dict()
        msg = "to_dict() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_instantiation_kwargs(self):
        """Tests instantiation with **kwargs."""
        obj = FileStorage()
        obj.name = "Holberton"
        obj.my_number = 89
        obj_json = obj.to_dict()
        new_obj = FileStorage(**obj_json)
        self.assertEqual(new_obj.to_dict(), obj.to_dict())

    def test_instantiation_dict(self):
        """Tests instantiation with **kwargs from custom dict."""
        d = {"__class__": "FileStorage",
             "updated_at":
             datetime(2132, 10, 26, 20, 23, 23, 123456).isoformat(),
             "created_at": datetime.now().isoformat(),
             "id": uuid.uuid4(),
             "var": "John",
             "int": 212,
             "float": 3.16}
        obj = FileStorage(**d)
        self.assertEqual(obj.to_dict(), d)

    def test_save_storage(self):
        """Tests that storage.save() is called from save()."""
        self.reset_storage()
        obj = FileStorage()
        obj.save()
        key = "{}.{}".format(type(obj).__name__, obj.id)
        d = {key: obj.to_dict()}
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path,
                  "r", encoding="utf-8") as f:
            self.assertEqual(len(f.read()), len(json.dumps(d)))
            f.seek(0)
            self.assertEqual(json.load(f), d)

    def test_save_with_many_args(self):
        """Tests save() with too many arguments."""
        self.reset_storage()
        with self.assertRaises(TypeError) as e:
            FileStorage.save(self, 98)
        msg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), msg)

    def test_save_no_args(self):
        """Tests save() with no arguments."""
        self.reset_storage()
        with self.assertRaises(TypeError) as e:
            FileStorage.save()
        msg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)


if __name__ == '__main__':
    unittest.main()
