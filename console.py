#!/usr/bin/python3
"""Entry point of the command interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User


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
                print("** class doesn't exist **")
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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
