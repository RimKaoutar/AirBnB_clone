#!/usr/bin/python3
"""Defines unittests for models/base_model.py.
Unittest classes:
    TestBaseModelInstantiate
    
"""

import contextlib
import os
import unittest
from datetime import datetime
from time import sleep

import models
from models.base_model import BaseModel


class TestBaseModelInstantiate(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self) -> None:
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self) -> None:
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self) -> None:
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self) -> None:
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self) -> None:
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self) -> None:
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_two_models_different_created_at(self) -> None:
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_two_models_different_updated_at(self) -> None:
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_str_representation(self) -> None:
        dt_obj = datetime.now()
        dt_repr = repr(dt_obj)
        base = BaseModel()
        base.id = "123456"
        base.created_at = base.updated_at = dt_obj
        bmstr = str(base)
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn(f"'created_at': {dt_repr}", bmstr)
        self.assertIn(f"'updated_at': {dt_repr}", bmstr)

    def test_args_unused(self) -> None:
        base = BaseModel(None)
        self.assertNotIn(None, base.__dict__.values())

    def test_instantiation_with_kwargs(self) -> None:
        dt_obj = datetime.now()
        dt_iso = dt_obj.isoformat()
        base = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(base.id, "345")
        self.assertEqual(base.created_at, dt_obj)
        self.assertEqual(base.updated_at, dt_obj)

    def test_instantiation_with_None_kwargs(self) -> None:
        """ must it be a type or value error?"""
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self) -> None:
        dt_obj = datetime.now()
        dt_iso = dt_obj.isoformat()
        base = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(base.id, "345")
        self.assertEqual(base.created_at, dt_obj)
        self.assertEqual(base.updated_at, dt_obj)

if __name__ == "__main__":
    unittest.main()