#!/usr/bin/python3
"""
Unit tests for console.py

Unittest classes:
    TestHBNBCommandQuit
    TestHBNBCommandEmptyLine
    TestHBNBCommandCreate
"""
import unittest
import os
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.engine.file_storage import FileStorage

class TestHBNBCommandQuit(unittest.TestCase):
    """Unittests for testing quiting the HBNB command interpreter."""

    def test_quit_exits(self) -> None:
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self) -> None:
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))

class TestHBNBCommandEmptyLine(unittest.TestCase):
    """Unittests for testing empty line in the HBNB command interpreter."""
    def test_emptyline_does_nothing(self) -> None:
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommandCreate(unittest.TestCase):
    """Unittests for testing create in the HBNB command interpreter."""

    @classmethod
    def setUp(self) -> None:
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self) -> None:
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class(self) -> None:
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_class(self) -> None:
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_objects(self) -> None:
        
        classes = ["BaseModel", "User", "State", "City", 
                   "Amenity", "Place", "Review"]

        for cls in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))
                self.assertLess(0, len(output.getvalue().strip()))
                test_key = f"{cls}.{output.getvalue().strip()}"
                self.assertIn(test_key, storage.all().keys())


                

        
if __name__ == "__main__":
    unittest.main()