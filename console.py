#!/usr/bin/python3
"""contains the entry point of the command interpreter"""

import cmd
import models.engine

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
        """Empty line shouldn't execute anything"""
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
            print(eval(arglist[0]().id))
            storage.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()