import os
import requests
import json

from openai import OpenAI  # 导入OpenAI库用于访问GPT模型
from logger import LOG  # 导入日志模块
from config import Config



class LLM:
    def __init__(self, config):
        """
        初始化 LLM 类，根据配置选择使用的模型（OpenAI、DeepSpeek 或 Ollama）
        """
        self.config = config
        self.model = config.llm_model_type.lower()
        if self.model == "openai":
            from openai import OpenAI
            self.client = OpenAI()
        elif self.model == "deepseek":
            from openai import OpenAI
            deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")  # 从环境变量中获取 DeepSeek API密钥
            self.client = OpenAI(api_key=deepseek_api_key, base_url=config.deepseek_api_url)
        elif self.model == "ollama":
            self.api_url = config.ollama_api_url
        else:
            raise ValueError(f"Unspported model type: {self.model}")
        
            # 从TXT文件加载提示信息
        with open("prompts/report_prompt.txt", "r", encoding='utf-8') as file:
            self.system_prompt = file.read()
        # 配置日志文件，当文件大小达到1MB时自动轮转，日志级别为DEBUG
        LOG.add("logs/llm_logs.log", rotation="1 MB", level="DEBUG")

    def generate_daily_report(self, markdown_content, dry_run=False):
        """
        生成每日报告，根据配置选择不同的模型来处理请求。
        
        :param markdown_content: 用户提供的Markdown内容。
        :param dry_run: 如果为True，提示信息将保存到文件而不实际调用模型。
        :return: 生成的报告内容或"DRY RUN"字符串。
        """
        
        # 使用从TXT文件加载的提示信息
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": markdown_content},
        ]

        if dry_run:
            # 如果启用了dry_run模式，将不会调用模型，而是将提示信息保存到文件中
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                # 格式化JSON字符串的保存
                json.dump(messages, f, indent=4, ensure_ascii=False)
            LOG.debug("Prompt saved to daily_progress/prompt.txt")
            return "DRY RUN"
        
        # 根据选择的模型调用相应的生成报告方法
        if self.model == "openai":
            return self._generate_report_openai(messages)
        elif self.model == "deepseek":
            return self._generate_report_deepseek(messages)
        elif self.model == "ollama":
            return self._generate_report_ollama(messages)
        else:
            raise ValueError(f"Unspported model type: {self.model}")
        
    def _generate_report_openai(self, messages):
        """
        使用 OpenAI GPT 模型生成报告。
        
        :param messages: 包含系统提示和用户内容的消息列表。
        :return: 生成的报告内容。
        """
        LOG.info("使用 OpenAI GPT 模型生成报告")
        try:
            response = self.client.chat.completions.create(
                model=self.config.openai_model_name,
                messages=messages,
            )
            LOG.debug("GPT 响应: {}", response)
            return response.choices[0].message.content
        except Exception as e:
            LOG.error(f"生成报告时发生错误：{e}")
            raise

    def _generate_report_deepseek(self, messages):
        """
        使用 DeepSeek 模型生成报告。
        """
        LOG.info("使用 DeepSeek 模型生成报告")
        try:
            response = self.client.chat.completions.create(
                model=self.config.deepseek_model_name,
                messages=messages,
            )
            LOG.debug("DeepSeek 响应: {}", response)
            return response.choices[0].message.content
        except Exception as e:
            LOG.error(f"生成报告时发生错误：{e}")
            raise

    def _generate_report_ollama(self, messages):
        """
        使用 Ollama 模型生成报告。
        """
        LOG.info("使用 Ollama 托管模型服务开始生成报告")
        try:
            palyload = {
                "model": self.config.ollama_model_name,
                "messages": messages,
                "stream": False,
            }
            response = requests.post(self.api_url, json=palyload)
            response_data = response.json()

            # 调试输出查看完整的响应结构
            LOG.debug("Ollama 响应: {}", response_data)

            # 直接从响应数据中获取 content
            message_content = response_data.get("message", {}).get("content", None)
            if message_content:
                return message_content
            else:
                LOG.error("Ollama 响应中未找到 content")
                raise ValueError("Ollama 响应中未找到 content")
        except Exception as e:
            LOG.error(f"生成报告时发生错误：{e}")
            raise

if __name__ == "__main__":
    config = Config()
    llm = LLM(config)
    
    markdown_content="""
# Progress for langchain-ai/langchain (2024-08-20 to 2024-08-21)


## Issues Closed in the Last 1 Days
- partners/chroma: release 0.1.3 #25599
- docs: few-shot conceptual guide #25596
- docs: update examples in api ref #25589
"""

    report = llm.generate_daily_report(markdown_content, dry_run=False)
    print(report)