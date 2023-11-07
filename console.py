#!/usr/bin/python3
"""contains the entry point of the command interpreter"""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """class HBNBCommand(cmd.Cmd)"""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    do_EOF = do_quit

    def emptyline(self):
        """Empty line + enter should not execute anything"""
        pass
    
    def do_create(self, args):
        """create an instance of a class type
        Args:
            args (obj): an object type, if no match in the
            classes list, output error
        """
        arglist = args.split()
        if len(arglist) == 0:
            print("** class name missing **")
        elif arglist[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arglist[0])().id)
            storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance."""
        if arg is None or arg == "":
            print("** class name missing **")
        else:
            args = arg.split()
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = f"{args[0]}.{args[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        if arg is None or arg == "":
            print("** class name missing **")
        else:
            args = arg.split()
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = f"{args[0]}.{args[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances,
        based or not on the class name."""
        args = arg.split()
        if len(args) == 0:
            all_instances = list(storage.all().values())
        else:
            class_name = args[0]
            if class_name not in storage.classes():
                print("** class doesn't exist **")
                return
            all_instances = [value for key, value in storage.all().items()
                             if key.startswith(class_name)]
        print([str(all_instance) for all_instance in all_instances])
    
    def do_update(self, args):
        """Updates an instance based on the class name and id by adding or updating attribute"""
        args = args.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in models.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in models.storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        if args[2] not in ["id", "created_at", "updated_at"]:
            setattr(models.storage.all()[key], args[2], type(getattr(models.storage.all()[key], args[2]))(args[3]))
            models.storage.all()[key].save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()