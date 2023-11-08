#!/usr/bin/python3
"""
Unit tests for console.py

Unittest classes:
    TestHBNBCommandQuit
    TestHBNBCommandEmptyLine
"""
import unittest
import os
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand


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


        
if __name__ == "__main__":
    unittest.main()