#!/usr/bin/env python3
"""parametrize a unit test"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
import requests
from typing import Dict, Tuple, Union
from utils import *


class TestAccessNestedMap(unittest.TestCase):
    """TestAccessNestedMap class"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ])
    def test_access_nested_map(
            self,
            nested_map: Dict,
            map_path: Tuple[str],
            expected_output: Union[int, Dict]) -> None:
        """Test access_nested_map"""
        self.assertEqual(access_nested_map(
            nested_map, map_path), expected_output)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict,
            map_path: Tuple[str],
            expected_output: Exception) -> None:
        """Test access_nested_map exception"""
        with self.assertRaises(expected_output):
            access_nested_map(nested_map, map_path)


class TestGetJson(unittest.TestCase):
    """ Test get json"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
        ])
    @patch('requests.get')
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict,
            mock_get) -> None:
        """Test get_json"""
        mock_get.return_value = Mock(json=lambda: test_payload)

        response = get_json(test_url)

        self.assertEqual(response, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test memoize"""
    def test_memoize(self) -> None:
        """Test memoize"""
        class TestClass:
            """Test class"""
            def a_method(self) -> int:
                """a method"""
                return 42

            @memoize
            def a_property(self) -> int:
                """a memoized method"""
                return self.a_method()

        with patch.object(
                TestClass,
                'a_method',
                return_value=lambda: 42) as mock_method:
            test = TestClass()
            self.assertEqual(test.a_property(), 42)
            self.assertEqual(test.a_property(), 42)
            mock_method.assert_called_once()
