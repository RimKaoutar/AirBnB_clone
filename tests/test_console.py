#!/usr/bin/python3
"""
Unit tests for console.py
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




        
if __name__ == "__main__":
    unittest.main()