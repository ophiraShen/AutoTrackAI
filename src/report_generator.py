# src/report_generator.py

import os
from llm import LLM

class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm

    def export_daily_progress(self, repo, updates):
        file_path = f'daily_progress/{repo.replace("/", "_")}_{date.today()}.md'
        with open(file_path, 'w') as file:
            file.write(f"# Daily Progress for {repo} ({date.today()})\n\n")
            file.write("## Commits\n")
            for commit in updates['commits']:
                file.write(f"- {commit}\n")
            file.write("\n## Issues\n")
            for issue in updates['issues']:
                file.write(f"- {issue}\n")
            file.write("\n## Pull Requests\n")
            for pr in updates['pull_requests']:
                file.write(f"- {pr}\n")
        return file_path

    def generate_daily_report(self, repo):
        markdown_file_path = f'daily_progress/{repo.replace("/", "_")}_{date.today()}.md'
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        report = self.llm.generate_daily_report(markdown_content)

        report_file_path = f'daily_reports/{repo.replace("/", "_")}_{date.today()}_report.md'
        with open(report_file_path, 'w') as report_file:
            report_file.write(report)

        print(f"Generated report saved to {report_file_path}")
