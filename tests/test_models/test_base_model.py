#!/usr/bin/python3
"""Unittest for BaseModel Class"""
import os
import re
import time
import json
import uuid
import unittest
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

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
        """Test instantiation with args"""
        obj = BaseModel()
        self.assertEqual(str(type(obj)),
                         "<class 'models.base_model.BaseModel'>")
        # A class is always an instance of itself
        self.assertIsInstance(obj, BaseModel)
        self.assertTrue(issubclass(type(obj), BaseModel))

    def test_init_no_args(self):
        """Testing __init__ with no arguments."""
        self.reset_storage()
        with self.assertRaises(TypeError) as e:
            BaseModel.__init__()
        msg = "__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_init_with_many_args(self):
        """Testing __init__ with many arguments."""
        self.reset_storage()
        args = [j for j in range(1000)]
        obj = BaseModel(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        obj = BaseModel(*args)

    def test_attributes(self):
        """Tests for attributes of BaseModel"""

        attrs = storage.attributes()["BaseModel"]
        obj = BaseModel()
        for k, v in attrs.items():
            self.assertTrue(hasattr(obj, k))
            self.assertEqual(type(getattr(obj, k, None)), v)

    def test_id(self):
        """Tests for unique ids."""
        uniq_ids = [BaseModel().id for i in range(1000)]
        self.assertEqual(len(set(uniq_ids)), len(uniq_ids))

    def test_datetime_created_at_updaed_at(self):
        """Testing difference btw  updated_at & created_at to make sure
        the current at creation"""
        date_now = datetime.now()
        obj = BaseModel()
        diff = obj.updated_at - obj.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        diff = obj.created_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.1)

    def test_save(self):
        """Tests save()"""
        obj = BaseModel()
        time.sleep(0.5)
        datenow = datetime.now()
        obj.save()
        diff = obj.updated_at - datenow
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_str(self):
        """Tests  __str__()"""
        obj = BaseModel()
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(str(obj))
        self.assertIsNotNone(res)
        self.assertEqual(res.group(1), "BaseModel")
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
        obj = BaseModel()
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
            BaseModel.to_dict(self, 98)
        msg = "to_dict() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), msg)

    def test_to_dict_with_no_args(self):
        """Tests to_dict() with no arguments."""
        self.reset_storage()
        with self.assertRaises(TypeError) as e:
            BaseModel.to_dict()
        msg = "to_dict() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_instantiation_kwargs(self):
        """Tests instantiation with **kwargs."""
        obj = BaseModel()
        obj.name = "Holberton"
        obj.my_number = 89
        obj_json = obj.to_dict()
        new_obj = BaseModel(**obj_json)
        self.assertEqual(new_obj.to_dict(), obj.to_dict())

    def test_instantiation_dict(self):
        """Tests instantiation with **kwargs from custom dict."""
        d = {"__class__": "BaseModel",
             "updated_at":
             datetime(2132, 10, 26, 20, 23, 23, 123456).isoformat(),
             "created_at": datetime.now().isoformat(),
             "id": uuid.uuid4(),
             "var": "John",
             "int": 212,
             "float": 3.16}
        obj = BaseModel(**d)
        self.assertEqual(obj.to_dict(), d)

    def test_save_storage(self):
        """Tests that storage.save() is called from save()."""
        self.reset_storage()
        obj = BaseModel()
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
            BaseModel.save(self, 98)
        msg = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), msg)

    def test_save_no_args(self):
        """Tests save() with no arguments."""
        self.reset_storage()
        with self.assertRaises(TypeError) as e:
            BaseModel.save()
        msg = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)


if __name__ == '__main__':
    unittest.main()
