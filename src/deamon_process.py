"""
这个模块的功能是创建一个后台守护进程（daemon process），用于定期运行调度器来执行特定任务，比如从GitHub获取数据、生成报告、发送通知等。
通过使用多线程和守护进程模式，它能够在后台持续运行，直到手动停止进程。模块中包含了配置加载、线程启动、守护进程化等步骤。
"""


import daemon  # 导入python-daemon模块，用于将程序转换为守护进程
import threading  # 导入线程模块，用于多线程执行任务
import time  # 导入时间模块，用于处理时间相关的操作

# 导入自定义的模块和类
from config import Config  # 配置类，负责加载配置信息
from github_client import GitHubClient  # 用于与GitHub API交互的客户端类
from notifier import Notifier  # 用于发送通知的类
from report_generator import ReportGenerator  # 用于生成报告的类
from llm import LLM  # 用于处理自然语言模型（LLM）的类
from subscription_manager import SubscriptionManager  # 用于管理订阅的类
from scheduler import Scheduler  # 调度器类，用于定时运行任务
from logger import LOG  # 日志模块，用于记录日志信息

# 函数：启动调度器
def run_scheduler(scheduler):
    scheduler.start()  # 调用调度器的start方法，开始执行定时任务

# 主函数：负责初始化各种组件，并启动守护进程
def main():
    # 加载配置文件
    config = Config()
    
    # 初始化GitHub客户端，用于访问GitHub API，传入GitHub Token
    github_client = GitHubClient(config.github_token)
    
    # 初始化通知模块，用于发送通知，传入配置中的通知设置
    notifier = Notifier(config.notification_settings)
    
    # 初始化语言模型（LLM），这个类可以用于生成自然语言报告或进行其他处理
    llm = LLM()
    
    # 初始化报告生成器，将语言模型传入，生成基于GitHub数据的报告
    report_generator = ReportGenerator(llm)
    
    # 初始化订阅管理器，传入配置中的订阅文件，管理用户或服务的订阅信息
    subscription_manager = SubscriptionManager(config.subscriptions_file)
    
    # 初始化调度器，传入各个模块，设置时间间隔
    scheduler = Scheduler(
        github_client=github_client,  # GitHub客户端
        notifier=notifier,  # 通知模块
        report_generator=report_generator,  # 报告生成器
        subscription_manager=subscription_manager,  # 订阅管理器
        interval=config.update_interval  # 定时任务的时间间隔
    )
    
    # 创建一个新的线程来运行调度器，并将其设置为守护线程
    scheduler_thread = threading.Thread(target=run_scheduler, args=(scheduler,))
    scheduler_thread.daemon = True  # 设置为守护线程，主线程结束时自动退出
    scheduler_thread.start()  # 启动调度器线程
    
    # 记录日志，表示调度器线程已经启动
    LOG.info("Scheduler thread started.")
    
    # 使用python-daemon库，将整个进程转换为守护进程
    with daemon.DaemonContext():
        try:
            # 守护进程的主循环，定期休眠直到被中断（例如Ctrl+C）
            while True:
                time.sleep(config.update_interval)  # 每隔一段时间（配置中的间隔）休眠
        except KeyboardInterrupt:
            # 捕捉到键盘中断信号时，记录日志并停止守护进程
            LOG.info("Daemon process stopped.")

# 如果脚本是直接运行的（而不是被导入），执行主函数
if __name__ == '__main__':
    main()
