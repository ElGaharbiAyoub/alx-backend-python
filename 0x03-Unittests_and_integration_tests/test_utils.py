#!/usr/bin/env python3
"""parametrize a unit test"""
import unittest
from parameterized import parameterized
from utils import *


class TestAccessNestedMap(unittest.TestCase):
    """TestAccessNestedMap class"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ])
    def test_access_nested_map(self, nested_map, map_path, expected_output):
        """Test access_nested_map"""
        self.assertEqual(access_nested_map(
            nested_map, map_path), expected_output)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, map_path , expected_output):
        """Test access_nested_map exception"""
        with self.assertRaises(expected_output):
            access_nested_map(nested_map, map_path)
