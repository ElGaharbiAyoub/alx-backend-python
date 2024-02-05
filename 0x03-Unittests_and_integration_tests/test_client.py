#!/usr/bin/env python3
"""
Test client module
"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class
    """
    @parameterized.expand([
        ("google",),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, org, mock_get):
        """Test org"""
        test_class = GithubOrgClient(org)
        test_class.org()
        mock_get.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )
