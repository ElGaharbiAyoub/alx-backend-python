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
    def test_get_json(self, test_url, test_payload, mock_get):
        mock_get.return_value = Mock(json=lambda: test_payload)

        response = get_json(test_url)

        self.assertEqual(response, test_payload)
        mock_get.assert_called_once_with(test_url)
