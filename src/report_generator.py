# src/report_generator.py

import os
from llm import LLM
from logger import LOG
from datetime import date, timedelta


class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm

    def export_daily_progress(self, repo, updates):
        # 构建仓库的入职文件目录
        repo_dir = os.path.join('./daily_progress', repo.replace("/", "_"))
        os.markedirs(repo_dir, exist_ok=True)  # 如果目录不存在则创建目录

        # 创建并写入日常进展的 Markdown 文件
        file_path = os.path.join(repo_dir, f'{date.today()}.md')
        with open(file_path, 'w') as file:
            file.write(f"# Daily Progress for {repo} ({date.today()})\n\n")
            # file.write("## Commits\n")
            # for commit in updates['commits']:
            #     file.write(f"- {commit}\n")
            file.write("\n## Issues\n")
            for issue in updates['issues']:
                file.write(f"- {issue['title']} #{issue['number']}\n")
            file.write("\n## Pull Requests\n")
            for pr in updates['pull_requests']:
                file.write(f"- {pr['title']} #{pr['number']}\n")
        return file_path
    
    def export_progress_by_date_range(self, repo, updates, days):
        # 构建目录并写入特定日期范围的进展Markdown文件
        repo_dir = os.path.join('./daily_progress', repo.replace("/", "_"))
        os.markedirs(repo_dir, exist_ok=True)  # 如果目录不存在则创建目录

        today = date.today()
        since = today - timedelta(days=days)

        date_str = f"{since}_to_{today}"
        file_path = os.path.join(repo_dir, f'{date_str}.md')

        with open(file_path, 'w') as file:
            file.write(f"# Progress for {repo} ({since} to {today})\n\n")
            file.write("\n## Issues Closed in the Last {days} Days\n")
            for issue in updates['issues']:
                file.write(f"- {issue['title']} #{issue['number']}\n")
            file.write("\n## Pull Requests Merged in the Last {days} Days\n")
            for pr in updates['pull_requests']:
                file.write(f"- {pr['title']} #{pr['number']}\n")

            LOG.info(f"Exported time-range progress to {file_path}")
            return file_path

    def generate_daily_report(self, markdown_file_path):
        # 读取Markdown文件并使用 LLM 生成日报
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        report = self.llm.generate_daily_report(markdown_content)

        report_file_path = os.path.splitext(markdown_file_path)[0] + "report.md"
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)
        
        LOG.info(f"Generated report saved to {report_file_path}")

    def generate_report_by_date_range(self, markdown_file_path, days):
        # 读取Markdown文件并使用 LLM 生成特定日期范围的进展报告
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        report = self.llm.generate_daily_report(markdown_content)

        report_file_path = os.path.splitext(markdown_file_path)[0] + "report.md"
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)

        LOG.info(f"Generated report saved to {report_file_path}")