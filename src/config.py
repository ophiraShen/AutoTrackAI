import json
import os

class Config:
    def __init__(self):
        try:
            self.load_config()
        except Exception as e:
            print(f"配置加载失败: {str(e)}")  # 或使用日志记录
            raise  # 重新抛出异常以便在主程序中捕获
    
    def load_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            
            self.email = config.get('email', {})
            self.email['password'] = os.getenv('EMAIL_PASSWORD', self.email.get('password', ''))

            # 加载 GitHub 相关配置
            github_config = config.get('github', {})
            self.github_token = os.getenv('GITHUB_TOKEN', github_config.get('token'))
            self.subscriptions_file = github_config.get('subscriptions_file')
            self.freq_days = github_config.get('progress_frequency_days', 1)
            self.exec_time = github_config.get('progress_execution_time', "08:00")

            # 加载 LLM 相关配置
            llm_config = config.get('llm', {})
            self.llm_model_type = llm_config.get('model_type', 'openai')
            self.openai_model_name = llm_config.get('openai_model_name', 'gpt-4o-mini')
            self.deepseek_model_name = llm_config.get('deepseek_model_name', 'deepseek-chat')
            self.deepseek_api_url = llm_config.get('deepseek_api_url', 'https://api.deepseek.com')
            self.ollama_model_name = llm_config.get('ollama_model_name', 'llama3')
            self.ollama_api_url = llm_config.get('ollama_api_url', 'http://localhost:11434/api/chat')
            
            # 加载报告类型配置
            self.report_types = config.get('report_types', ["github", "hacker_news"])  # 默认报告类型
            
            # 加载 Slack 配置
            slack_config = config.get('slack', {})
            self.slack_webhook_url = slack_config.get('webhook_url')

if __name__ == "__main__":
    config = Config()
    print(config.github_token)
    print(config.email)
    print(config.subscriptions_file)
    print(config.freq_days)
    print(config.exec_time)