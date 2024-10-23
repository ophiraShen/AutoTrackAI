import sys
import os
import unittest
from unittest.mock import patch, MagicMock


# 添加 src 目录到模块搜索路径，以便可以导入 src 目录中的模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from github_client import GitHubClient

class TestGitHubClient(unittest.TestCase):
    def setUp(self):
        self.token = "fake_token"
        self.client = GitHubClient(self.token)
        self.repo = "DjangoPeng/openai-quickstart"

    @patch('github_client.requests.get')
    def test_fetch_commits(self, mock_get):
        """
        测试 fetch_commits 方法是否正确获取提交记录。
        """
        # 模拟 API 响应
        mock_response = MagicMock()
        mock_response.json.return_value = [{"sha": "abc123", "commit": {"message": "Initial commit"}}]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # 调用 fetch_commits 方法, 并进行断言检查
        commits = self.client.fetch_commits(self.repo)
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0]['sha'], 'abc123')
        self.assertEqual(commits[0]['commit']['message'], 'Initial commit')

    @patch('github_client.requests.get')
    def test_fetch_issues(self, mock_get):
        """
        测试 fetch_issues 方法是否正确获取问题记录。
        """
        # 模拟 API 响应
        mock_response = MagicMock()
        mock_response.json.return_value = [{"number": 1, "title": "Fix bug"}]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # 调用 fetch_issues 方法, 并进行断言检查
        issues = self.client.fetch_issues(self.repo)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['number'], 1)
        self.assertEqual(issues[0]['title'], 'Fix bug')

    @patch('github_client.requests.get')
    def test_fetch_pull_requests(self, mock_get):
        """
        测试 fetch_pull_requests 方法是否正确获取拉取请求记录。
        """
        # 模拟 API 响应
        mock_response = MagicMock()
        mock_response.json.return_value = [{"number": 42, "title": "Add new feature"}]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # 调用 fetch_pull_requests 方法, 并进行断言检查
        pull_requests = self.client.fetch_pull_requests(self.repo)
        self.assertEqual(len(pull_requests), 1)
        self.assertEqual(pull_requests[0]['number'], 42)
        self.assertEqual(pull_requests[0]['title'], 'Add new feature')

    @patch('github_client.requests.get')
    def test_export_daily_progress(self, mock_get):
        """
        测试 export_daily_progress 方法是否正确导出每日进度。
        """
        # 模拟 API 响应
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # 调用 export_daily_progress 方法, 并进行断言检查
        file_path = self.client.export_daily_progress(self.repo)
        self.assertTrue(file_path.endswith('.md'))

    @patch('github_client.requests.get')
    def test_export_progress_by_date_range(self, mock_get):
        """
        测试 export_progress_by_date_range 方法是否正确导出指定日期范围内的进度。
        """
        # 模拟 API 响应
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # 调用 export_progress_by_date_range 方法, 并进行断言检查
        file_path = self.client.export_progress_by_date_range(self.repo, 7)
        self.assertTrue(file_path.endswith('.md'))
        

if __name__ == '__main__':
    unittest.main()

