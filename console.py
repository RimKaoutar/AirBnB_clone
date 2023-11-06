#!/usr/bin/python3
"""contains the entry point of the command interpreter"""

import cmd

class HBNBCommand(cmd.Cmd):
    """class HBNBCommand(cmd.Cmd)"""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    do_EOF = do_quit

    def emptyline(self):
        """Empty line shouldn't execute anything"""
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()