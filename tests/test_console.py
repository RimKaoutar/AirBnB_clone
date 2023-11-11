#!/usr/bin/python3
"""
Unit tests for console.py

Unittest classes:
    TestHBNBCommandQuit
    TestHBNBCommandEmptyLine
    TestHBNBCommandCreate
    TestHBNBCommandPrompt
    TestHBNBCommandDestroy
    TestHBNBCommandAll
    TestHBNBCommandUpdate
    TestHBNBCommandCount
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

    def test_destroy_id_missing_dot_notation(self) -> None:
        correct = "** instance id missing **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.destroy()"))

    def test_destroy_invalid_id_space_notation(self) -> None:
        correct = "** no instance found **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"destroy {cls} 1"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_id_dot_notation(self) -> None:
        correct = "** no instance found **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.destroy(1)"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_objects_space_notation(self) -> None:
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()[f"{cls}.{test_id}"]
                command = f"destroy {cls} {test_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(obj, storage.all())

    def test_destroy_objects_dot_notation(self) -> None:
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()["{}.{}".format(cls,test_id)]
                command = "{}.destroy({})".format(cls,test_id)
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(obj, storage.all())
    

class TestHBNBCommandAll(unittest.TestCase):
    """Unittests for testing all of the HBNB command interpreter."""

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

    def test_all_invalid_class(self) -> None:
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all ALX"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_all_objects_space_notation(self) -> None:
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all"))
                self.assertIn(f"{cls}", output.getvalue().strip())
    

    def test_all_single_object_space_notation(self) -> None:
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())

    def test_all_single_object_dot_notation(self) -> None:
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())

class TestHBNBCommandUpdate(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""

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

    def test_update_missing_class(self) -> None:
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_update_invalid_class(self) -> None:
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_id_space_notation(self) -> None:
        correct = "** instance id missing **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"update {cls}"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_id_dot_notation(self) -> None:
        correct = "** instance id missing **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.update()"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_invalid_id_space_notation(self) -> None:
        correct = "** no instance found **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"update {cls} 1"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_invalid_id_dot_notation(self) -> None:
        correct = "** no instance found **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.update(1)"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_name_space_notation(self) -> None:
        correct = "** attribute name missing **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))
                test_id = output.getvalue().strip()
                test_cmd = "update {} {}".format(cls, test_id)
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(test_cmd))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_name_dot_notation(self) -> None:
        correct = "** attribute name missing **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))
                test_id = output.getvalue().strip()
                test_cmd = "{}.update({})".format(cls, test_id)
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(test_cmd))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_value_space_notation(self) -> None:
        correct = "** value missing **"
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd(f"create {cls}")
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                test_cmd = "update {} {} attr_name".format(cls, test_id)
                self.assertFalse(HBNBCommand().onecmd(test_cmd))
                self.assertEqual(correct, output.getvalue().strip())

class TestHBNBCommandCount(unittest.TestCase):
    """Unittests for testing count in HBNB comand interpreter."""

    classes = ["BaseModel", "User", "State", "City", 
               "Amenity", "Place", "Review"]

    @classmethod
    def setUp(self) -> None:
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

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

    def test_count_object(self) -> None:
        for cls in self.classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.count()"))
                self.assertEqual("1", output.getvalue().strip())




























if __name__ == "__main__":
    unittest.main()