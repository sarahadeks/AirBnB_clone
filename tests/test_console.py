import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os


class TestHBNBCommand(unittest.TestCase):
    def setUp(self):
        self.console = HBNBCommand()

    def tearDown(self):
        pass

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("quit"))
            output = f.getvalue().strip()
            self.assertEqual(output, "")

    def test_help(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("help"))
            output = f.getvalue().strip()
            self.assertIn("Documented commands (type help <topic>):", output)
            self.assertIn("EOF  help  quit", output)

    def test_create(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("create"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("create UnknownClass"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("create BaseModel"))
            output = f.getvalue().strip()
            self.assertRegex(output, r"^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$")
            # Clean up created instance
            obj_id = output
            filename = "file.json"
            storage.delete_file(filename)
            self.assertFalse(os.path.isfile(filename))

    def test_show(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("show"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("show UnknownClass"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("show BaseModel"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("show BaseModel 12345"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("show BaseModel {}".format(obj_id)))
            output = f.getvalue().strip()
            self.assertRegex(output, r"^\[BaseModel\] \({}\) ".format(obj_id))

        # Clean up created instance
        filename = "file.json"
        storage.delete_file(filename)
        self.assertFalse(os.path.isfile(filename))

    def test_destroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("destroy"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("destroy UnknownClass"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("destroy BaseModel"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("destroy BaseModel 12345"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("destroy BaseModel {}".format(obj_id)))
            output = f.getvalue().strip()
            self.assertEqual(output, "")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("show BaseModel {}".format(obj_id)))
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

        # Clean up created instance
        filename = "file.json"
        storage.delete_file(filename)
        self.assertFalse(os.path.isfile(filename))

    def test_all(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("all UnknownClass"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("create User"))
            user_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("all"))
            output = f.getvalue().strip()
            self.assertIn("[BaseModel] ({})".format(obj_id), output)
            self.assertIn("[User] ({})".format(user_id), output)
            self.assertIn("[State] ({})".format(state_id), output)

        # Clean up created instances
        filename = "file.json"
        storage.delete_file(filename)
        self.assertFalse(os.path.isfile(filename))

    def test_update(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("update"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("update UnknownClass"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("update BaseModel"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("update BaseModel 12345"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd('update BaseModel {} name "John"'.format(obj_id)))
            output = f.getvalue().strip()
            self.assertEqual(output, "")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("show BaseModel {}".format(obj_id)))
            output = f.getvalue().strip()
            self.assertIn("'name': 'John'", output)

        # Clean up created instance
        filename = "file.json"
        storage.delete_file(filename)
        self.assertFalse(os.path.isfile(filename))

    def test_update_dict(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("update"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("update UnknownClass"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("update BaseModel"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("update BaseModel 12345"))
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("create BaseModel"))
            obj_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd('update BaseModel {} {"name": "John", "age": 30}'.format(obj_id)))
            output = f.getvalue().strip()
            self.assertEqual(output, "")

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("show BaseModel {}".format(obj_id)))
            output = f.getvalue().strip()
            self.assertIn("'name': 'John'", output)
            self.assertIn("'age': 30", output)

        # Clean up created instance
        filename = "file.json"
        storage.delete_file(filename)
        self.assertFalse(os.path.isfile(filename))


if __name__ == "__main__":
    unittest.main()
