# src/llm.py
from openai import OpenAI
from logger import LOG


class LLM:
    def __init__(self, model="gpt-3.5-turbo"):
        self.client = OpenAI()
        self.model = model
        LOG.add("daily_progress/llm_logs.log", rotation="1 MB", level="DEBUG")


    def generate_daily_report(self, markdown_content, dry_run=False):

        system_prompt = f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题."

        if dry_run:
            # This is a dry run. No report generated.
            LOG.info("Dry run model enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                f.write(system_prompt + "\n\n" + markdown_content)
            LOG.debug("Prompt saved to daily_progress/prompt.txt")
            return "DRY RUN"

        LOG.info(f"Starting report generation using model: {self.model}.")

        user_prompt = markdown_content

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )
            LOG.debug(f"{self.model} response: {response}")
            return response.choices[0].message.content

        except Exception as e:
            LOG.error("An error occurred while generation the report: {}", e)
            raise

