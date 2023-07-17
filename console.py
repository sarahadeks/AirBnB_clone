#!/usr/bin/python3
"""Entry point of the command interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import re
import json
import ast


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class"""

    prompt = "(hbnb) "

    def do_quit(self, args):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """Exit on EOF (ctrl+D)
        """
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered
        """
        pass

    def do_create(self, arg):
        """Create a new instance of the class passed
        """
        if not arg:
            print("** class name missing **")
        elif arg not in storage.class_map:
            print("** class doesn't exist **")
        else:
            obj = storage.class_map[arg]()
            obj.save()
            print(obj.id)

    def do_show(self, arg):
        """Print the string representation of an instance based
        on the class name and id
        """
        if not arg:
            print("** class name missing **")
        else:
            args = arg.split()
            # making sure the object exists
            if args[0] not in storage.class_map:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                obj_key = "{}.{}".format(args[0], args[1])
                if obj_key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[obj_key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        (save the change into the JSON file).
        """
        if not arg:
            print("** class name missing **")
        else:
            args = arg.split()
            if args[0] not in storage.class_map:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                obj_key = "{}.{}".format(args[0], args[1])
                if obj_key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[obj_key]
                    storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        all_objs = storage.all()
        if arg != "":
            args = arg.split()
            if args[0] not in storage.class_map:
                print("** class doesn't exist **")
            else:
                cls_name = args[0]
                objs_of_cls = [str(obj) for obj in all_objs.values()
                               if obj.__class__.__name__ == cls_name]
                print(objs_of_cls)
        else:
            objs_of_cls = [str(obj) for obj in all_objs.values()]
            print(objs_of_cls)

    def do_update(self, arg):
        """Update an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if args[0] not in storage.class_map:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_key = "{}.{}".format(args[0], args[1])
        all_objs = storage.all()

        if obj_key not in all_objs:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        attr_name = args[2]
        attr_value = args[3]

        obj = all_objs[obj_key]
        if hasattr(obj, attr_name):
            # getattr returns the value associated with the attr_name
            attr_type = type(getattr(obj, attr_name))
            # since inputs from the command line are by default str, we
            # we would want to cast our values to the proper types
            setattr(obj, attr_name, attr_type(attr_value))
        else:
            if attr_value.startswith('"') and attr_value.endswith('"'):
                attr_value = attr_value[1:-1]
            elif attr_value.startswith("'") and attr_value.endswith("'"):
                attr_value = attr_value[1:-1]
            else:
                if attr_value.isdigit():
                    attr_value = int(attr_value)
                elif "." in attr_value:
                    try:
                        attr_value = float(attr_value)
                    except ValueError:
                        pass
            setattr(obj, attr_name, (attr_value))
            obj.save()

    def correctdefault(self, line):
        """Called on an input line when the command prefix is not recognized"""
        pattern_all = r"^(\w+)\.all\(\)$"
        pattern_count = r"^(\w+)\.count\(\)$"
        pattern_show = r"^(\w+)\.show\(\"([\w-]+)\"\)$"
        pattern_destroy = r"^(\w+)\.destroy\(\"([\w-]+)\"\)$"

        match_all = re.match(pattern_all, line)
        match_count = re.match(pattern_count, line)
        match_show = re.match(pattern_show, line)
        match_destroy = re.match(pattern_destroy, line)

        if match_all:
            class_name = match_all.group(1)
            self.get_all_instances(class_name)
        elif match_count:
            class_name = match_count.group(1)
            self.get_instance_count(class_name)
        elif match_show:
            class_name = match_show.group(1)
            instance_id = match_show.group(2)
            self.get_instance_by_id(class_name, instance_id)
        elif match_destroy:
            class_name = match_destroy.group(1)
            instance_id = match_destroy.group(2)
            self.destroy_instance(class_name, instance_id)
        else:
            print("*** Unknown syntax: {}".format(line))

    def default(self, line):
        """Called on an input line when the command prefix is not recognized"""
        pattern_all = r"^(\w+)\.all\(\)$"
        pattern_count = r"^(\w+)\.count\(\)$"
        pattern_show = r"^(\w+)\.show\(\"([\w-]+)\"\)$"
        pattern_destroy = r"^(\w+)\.destroy\(\"([\w-]+)\"\)$"
        pattern_update = r"^(\w+)\.update\(\"([\w-]+)\"\s*,\s*\"([\w-]+)\"\s*,\s*(.*)\)$"
        pattern_update_dict = r'^(\w+)\.update\("([\w-]+)"\s*,\s*(\{.*\})\)$'

        match_all = re.match(pattern_all, line)
        match_count = re.match(pattern_count, line)
        match_show = re.match(pattern_show, line)
        match_destroy = re.match(pattern_destroy, line)
        match_update = re.match(pattern_update, line)
        match_update_dict = re.match(pattern_update_dict, line)

        if match_all:
            class_name = match_all.group(1)
            self.get_all_instances(class_name)
        elif match_count:
            class_name = match_count.group(1)
            self.get_instance_count(class_name)
        elif match_show:
            class_name = match_show.group(1)
            instance_id = match_show.group(2)
            self.get_instance_by_id(class_name, instance_id)
        elif match_destroy:
            class_name = match_destroy.group(1)
            instance_id = match_destroy.group(2)
            self.destroy_instance(class_name, instance_id)
        elif match_update:
            class_name = match_update.group(1)
            instance_id = match_update.group(2)
            attr_name = match_update.group(3)
            attr_value = match_update.group(4)
            self.update_instance(class_name, instance_id, attr_name, attr_value)
        elif match_update_dict:
            class_name = match_update_dict.group(1)
            instance_id = match_update_dict.group(2)
            attr_dict_str = match_update_dict.group(3)
            attr_dict = ast.literal_eval(attr_dict_str)
            self.update_instance_dict(class_name, instance_id, attr_dict)
        else:
            print("*** Unknown syntax: {}".format(line))

    def get_all_instances(self, class_name):
        """Retrieve all instances of a class"""
        if class_name not in storage.class_map:
            print("** class doesn't exist **")
            return

        instances = storage.all().values()
        class_instances = [str(instance) for instance in instances if isinstance(instance, storage.class_map[class_name])]
        print(class_instances)

    def get_instance_count(self, class_name):
        """Retrieve the number of instances of a class"""
        if class_name not in storage.class_map:
            print("** class doesn't exist **")
            return

        instances = storage.all().values()
        count = sum(1 for instance in instances if isinstance(instance, storage.class_map[class_name]))
        print(count)

    def get_instance_by_id(self, class_name, instance_id):
        """Retrieve an instance based on its ID"""
        if class_name not in storage.class_map:
            print("** class doesn't exist **")
            return

        key = "{}.{}".format(class_name, instance_id)
        instance = storage.all().get(key)
        if instance:
            print(instance)
        else:
            print("** no instance found **")

    def destroy_instance(self, class_name, instance_id):
        """Destroy an instance based on its ID"""
        if class_name not in storage.class_map:
            print("** class doesn't exist **")
            return

        key = "{}.{}".format(class_name, instance_id)
        instances = storage.all()

        if key not in instances:
            print("** no instance found **")
            return

        del instances[key]
        storage.save()

    def update_instance(self, class_name, instance_id, attr_name, attr_value):
        """Update an instance based on its ID"""
        if class_name not in storage.class_map:
            print("** class doesn't exist **")
            return

        key = "{}.{}".format(class_name, instance_id)
        instances = storage.all()

        if key not in instances:
            print("** no instance found **")
            return

        obj = instances[key]
        setattr(obj, attr_name, eval(attr_value))
        obj.save()

    def update_instance_dict(self, class_name, instance_id, attr_dict):
        """Update an instance based on its ID with a dictionary"""
        if class_name not in storage.class_map:
            print("** class doesn't exist **")
            return

        key = "{}.{}".format(class_name, instance_id)
        instances = storage.all()

        if key not in instances:
            print("** no instance found **")
            return

        obj = instances[key]

        for attr_name, attr_value in attr_dict.items():
            setattr(obj, attr_name, attr_value)

        obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
