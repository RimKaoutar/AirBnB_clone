#!/usr/bin/python3
"""
Unit tests for console.py

Unittest classes:
    TestHBNBCommandQuit
    TestHBNBCommandEmptyLine
    TestHBNBCommandCreate
    TestHBNBCommandPrompt
    TestHBNBCommandDestroy
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

class TestHBNBCommandPrompt(unittest.TestCase):
    """Unittests for testing prompting the HBNB command interpreter."""

    def test_prompt_string(self) -> None:
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

class TestHBNBCommandShow(unittest.TestCase):
    """Unittests for testing show in the HBNB command interpreter"""

    classes = ["BaseModel", "User", "State", "City", 
               "Amenity", "Place", "Review"]

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

    def test_show_missing_class(self) -> None:
        expected = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(expected, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(expected, output.getvalue().strip())

    def test_show_invalid_class(self) -> None:
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_id_space_notation(self) -> None:
        correct = "** instance id missing **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"show {cls}"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_id_dot_notation(self) -> None:
        correct = "** instance id missing **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.show()"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_no_instance_found_space_notation(self) -> None:
        correct = "** no instance found **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"show {cls} 1"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_no_instance_found_dot_notation(self) -> None:
        correct = "** no instance found **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.show(1)"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_objects_space_notation(self) -> None:
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()[f"{cls}.{test_id}"]
                command = f"show {cls} {test_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())

class TestHBNBCommandDestroy(unittest.TestCase):
    """Unittests for testing destroy in the HBNB command interpreter."""

    classes = ["BaseModel", "User", "State", "City", 
               "Amenity", "Place", "Review"]

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
        storage.reload()

    def test_destroy_missing_class(self) -> None:
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_class(self) -> None:
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_id_missing_space_notation(self) -> None:
        correct = "** instance id missing **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"destroy {cls}"))
                self.assertEqual(correct, output.getvalue().strip())
        









if __name__ == "__main__":
    unittest.main()