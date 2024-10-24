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
        # 从环境变量获取GitHub Token
        self.github_token = os.getenv('GITHUB_TOKEN')
        
        with open('config.json', 'r') as f:
            config = json.load(f)
            
            # 如果环境变量中没有GitHub Token，则从配置文件中读取
            if not self.github_token:
                self.github_token = config.get('github_token')
                
            # 初始化电子邮件设置
            self.email = config.get('email', {})
            # 使用环境变量或配置文件中的电子邮件密码
            self.email['password'] = os.getenv('EMAIL_PASSWORD', self.email.get('password', ''))

            self.subscriptions_file = config.get('subscriptions_file')
            # 默认每天执行
            self.freq_days = config.get('github_progress_frequency_days', 1)
            # 默认早上8点更新 (操作系统默认时区是 UTC +0，08点刚好对应北京时间凌晨12点)
            self.exec_time = config.get('github_progress_execution_time', "08:00")

            # 初始化LLM设置
            llm_config = config.get('llm', {})
            self.llm_model_type = llm_config.get('model_type', 'deepseek')
            self.openai_model_name = llm_config.get('openai_model_name', 'gpt-4o-mini')
            self.ollama_model_name = llm_config.get('ollama_model_name', 'llama3.1')
            self.deepseek_model_name = llm_config.get('deepseek_model_name', 'deepseek-chat')
            self.ollama_api_url = llm_config.get('ollama_api_url', 'http://localhost:11434/api/chat')
            self.deepseek_api_url = llm_config.get('deepseek_api_url', 'https://api.deepseek.com')

if __name__ == "__main__":
    config = Config()
    print(config.github_token)
    print(config.email)
    print(config.subscriptions_file)
    print(config.freq_days)
    print(config.exec_time)