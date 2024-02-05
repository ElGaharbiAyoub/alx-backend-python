#!/usr/bin/env python3
"""parametrize a unit test"""
import unittest
from parameterized import parameterized
from utils import *


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": {"b": {"c": 1}}}, ["a", "b", "c"], 1),
        ({"x": {"y": {"z": 2}}}, ["x", "y", "z"], 2),
    ])
    def test_access_nested_map(self, nested_map, map_path, expected_output):
        self.assertEqual(access_nested_map(nested_map, map_path), expected_output)
