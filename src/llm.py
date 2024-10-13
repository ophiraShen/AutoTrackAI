# src/llm.py

from openai import OpenAI
import openai


class LLM:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=self.api_key)


    def generate_daily_report(self, markdown_content):
        system_prompt = f"Please summarize the following project updates into a formal daily report."

        user_prompt = markdown_content

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )

        return response.choices[0].message.content
