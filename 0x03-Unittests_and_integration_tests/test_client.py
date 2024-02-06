#!/usr/bin/env python3
"""
Test client module
"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
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

    @parameterized.expand([
        ("google", "repos_url", "http://google.com"),
        ("abc", "repos_url", "http://abc.com"),
    ])
    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, org, property_name, expected, mock_org):
        """Test public repos url"""
        mock_org.return_value = {property_name: expected}
        test_class = GithubOrgClient(org)
        self.assertEqual(test_class._public_repos_url, expected)
        mock_org.assert_called_once_with()

    @patch(
        'client.get_json',
        return_value=[{"name": "repo1"}, {"name": "repo2"}])
    def test_public_repos(self, mock_get_json):
        with patch.object(
                GithubOrgClient,
                '_public_repos_url',
                new_callable=PropertyMock) as mock_p_r:
            mock_p_r.return_value = "\
                https://api.github.com/orgs/org_name/repos"

            github_org_client = GithubOrgClient("org_name")
            repos = github_org_client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2"])
            mock_p_r.assert_called_once()
            mock_get_json.assert_called_once()
