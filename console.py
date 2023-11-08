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
from re import search

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
        args = [i.strip(",") for i in args.split()]
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        if args[2] not in ["id", "created_at", "updated_at"]:
            setattr(storage.all()[key], args[2], type(getattr(storage.all()[key], args[2]))(args[3]).strip("\""))
            storage.all()[key].save()

    def do_count(self, arg):
        """count the number of instances of an object
        Args:
            arg (obj): the supposedly class to look for
        """
        args = [i.strip(".") for i in arg.split()]
        count = 0
        for obj in storage.all().values():
            if args[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def default(self, arg):
        """Default behavior for cmd module when 
        we enter <class_name>.<method> or invalid input"""
        
        """ <!> must update the methods when adding do_count() """
        methods = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
            "count": self.do_count
        }
        result = search(r"\.", arg)
        if result is not None:
            args = [arg[:result.span()[0]], arg[result.span()[1]:]]
            result = search(r"\((.*?)\)", args[1])
            if result is not None:
                cmd = [args[1][:result.span()[0]], result.group()[1:-1]]
                if cmd[0] in methods.keys():
                    call = f"{args[0]} {cmd[1]}"
                    return methods[cmd[0]](call)
        print(f"*** Unknown syntax: {arg}")
        return False

if __name__ == '__main__':
    HBNBCommand().cmdloop()