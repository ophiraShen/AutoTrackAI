import shlex  # 用于将用户输入的字符串分割成命令行参数列表

# 导入各个模块
from config import Config  # 配置管理模块，负责读取和存储配置
from github_client import GitHubClient  # 与 GitHub API 交互的客户端
from notifier import Notifier  # 通知模块，用于发送通知
from report_generator import ReportGenerator  # 负责生成报告的模块
from llm import LLM  # LLM（大语言模型）模块，可能用于生成自然语言报告
from subscription_manager import SubscriptionManager  # 订阅管理模块
from command_handler import CommandHandler  # 命令处理模块
from logger import LOG  # 日志模块，用于记录错误和调试信息

def main():
    # 初始化配置，读取配置文件中的 GitHub Token 和通知设置
    config = Config()
    
    # 创建 GitHub API 客户端，使用从配置文件读取的 GitHub 令牌进行身份验证
    github_client = GitHubClient(config.github_token)
    
    # 初始化通知模块，传递通知设置
    notifier = Notifier(config.notification_settings)
    
    # 初始化 LLM 模块，可能用于生成报告的内容
    llm = LLM()
    
    # 初始化报告生成器，依赖 LLM 模块
    report_generator = ReportGenerator(llm)
    
    # 初始化订阅管理器，用于管理订阅的 GitHub 项目
    subscription_manager = SubscriptionManager(config.subscriptions_file)
    
    # 初始化命令处理器，将 GitHub 客户端、订阅管理器和报告生成器传递给命令处理模块
    command_handler = CommandHandler(github_client, subscription_manager, report_generator)
    
    # 获取命令行解析器，定义了所有可用命令及其参数
    parser = command_handler.parser
    
    # 打印帮助信息，列出所有支持的命令
    command_handler.print_help()

    # 进入命令行交互模式
    while True:
        try:
            # 等待用户输入
            user_input = input("GitHub Sentinel> ")
            
            # 如果用户输入 'exit' 或 'quit'，则退出循环，结束程序
            if user_input in ['exit', 'quit']:
                break
            
            try:
                # 使用 shlex 分割用户输入的命令，将其解析为命令行参数
                args = parser.parse_args(shlex.split(user_input))
                
                # 如果未输入任何命令，跳过这次循环
                if args.command is None:
                    continue
                
                # 执行与输入命令关联的函数
                args.func(args)
            except SystemExit as e:
                # 捕获解析命令行时的 SystemExit 异常，表示无效命令
                LOG.error("Invalid command. Type 'help' to see the list of available commands.")
        except Exception as e:
            # 捕获其他异常，记录错误日志
            LOG.error(f"Unexpected error: {e}")

# 如果脚本是直接运行的（而不是作为模块导入），则调用 main 函数启动程序
if __name__ == '__main__':
    main()
