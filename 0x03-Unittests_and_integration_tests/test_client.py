#!/usr/bin/env python3
"""
Test client module
"""
import unittest
from typing import List, Dict
from unittest.mock import patch, PropertyMock, MagicMock, Mock
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class
    """
    @parameterized.expand([
        ("google",),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, org, mock_get: MagicMock) -> None:
        """Test org"""
        test_class = GithubOrgClient(org)
        test_class.org()
        mock_get.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    def test_public_repos_url(self) -> None:
        """Tests the `_public_repos_url` property."""
        with patch(
                "client.GithubOrgClient.org",
                new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos",
            )

    @patch(
        'client.get_json',
        return_value=[{"name": "repo1"}, {"name": "repo2"}])
    def test_public_repos(self, mock_get_json) -> None:
        """Test public repos"""
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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "not_my_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict, key: str,  expected) -> None:
        """Test has license"""
        github_org_client = GithubOrgClient("google")
        self.assertEqual(
            github_org_client.has_license(repo, key),
            expected
        )


@parameterized_class([
   {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    TestIntegrationGithubOrgClient class
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Set up class"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url: str) -> MagicMock:
            """Side effect"""
            mock_resp = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
                mock_resp.status_code = 200
            elif url == "https://api.github.com/orgs/google/repos":
                mock_resp.json.return_value = cls.repos_payload
                mock_resp.status_code = 200
            else:
                mock_resp.json.return_value = None
                mock_resp.status_code = 404
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class"""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test public repos"""
        github_org_client = GithubOrgClient("google")
        repos = github_org_client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test public repos with license"""
        github_org_client = GithubOrgClient("google")
        repos = github_org_client.public_repos("apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
