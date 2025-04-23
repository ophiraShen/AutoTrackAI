import gradio as gr

from config import Config
from github_client import GitHubClient
from hacker_news_client import HackerNewsClient
from report_generator import ReportGenerator
from llm import LLM
from subscription_manager import SubscriptionManager
from logger import LOG


config = Config()
github_client = GitHubClient(config.github_token)
hacker_news_client = HackerNewsClient()
subscription_manager = SubscriptionManager(config.subscriptions_file)

def generate_github_report(model_type, model_name, repo, days):
    config.llm_model_type = model_type

    if model_type == "openai":
        config.openai_model_name = model_name
    elif model_type == "deepseek":
        config.deepseek_model_name = model_name
    elif model_type == "ollama":
        config.ollama_model_name = model_name

    llm = LLM(config)
    report_generator = ReportGenerator(llm, config.report_types)

    raw_file_path = github_client.export_progress_by_date_range(repo, days)
    report, report_file_path = report_generator.generate_github_report(raw_file_path)
    return report, report_file_path

def generate_hn_hour_topic(model_type, model_name):
    config.llm_model_type = model_type

    if model_type == "openai":
        config.openai_model_name = model_name
    elif model_type == "deepseek":
        config.deepseek_model_name = model_name
    elif model_type == "ollama":
        config.ollama_model_name = model_name

    llm = LLM(config)
    report_generator = ReportGenerator(llm, config.report_types)

    raw_file_path = hacker_news_client.export_top_stories()
    report, report_file_path = report_generator.generate_hn_topic_report(raw_file_path)
    return report, report_file_path

def update_model_list(model_type):
    if model_type == "openai":
        return gr.Dropdown(choices=["gpt-4o", "gpt-4o-mini"], label="选择模型")
    elif model_type == "deepseek":
        return gr.Dropdown(choices=["deepseek-chat"], label="选择模型")
    elif model_type == "ollama":
        return gr.Dropdown(choices=[config.ollama_model_name], label="选择模型")


# 创建 gradio 应用
with gr.Blocks() as demo:
    # 创建 GitHub 项目报告的 UI
    with gr.Tab("GitHub 项目报告"):
        gr.Markdown("## GitHub 项目进展")

        model_type = gr.Radio(choices=["openai", "deepseek", "ollama"], label="模型类型",
                              info="使用 OpenAI、DeepSeek API 或 Ollama 私有化模型服务")
        
        model_name = gr.Dropdown(choices=["gpt-4o", "gpt-4o-mini"], label="选择模型")

        subscription_list = gr.Dropdown(choices=subscription_manager.list_subscriptions(), label="订阅列表",
                                        info="已订阅的 GitHub 项目列表")
        
        days = gr.Slider(value=2, minimum=1, maximum=7, step=1, label="报告周期", info="生产项目过去一段时间进展，单位：天")

        # 使用 radio 组件的值来更新 dropdown 组件的选项
        model_type.change(fn=update_model_list, inputs=model_type, outputs=model_name)

        button = gr.Button(value="生成报告", variant="primary")

        markdown_output = gr.Markdown(label="报告输出")
        file_ouput = gr.File(label="下载报告")

        # 绑定按钮点击事件
        button.click(fn=generate_github_report, inputs=[model_type, model_name, subscription_list, days], outputs=[markdown_output, file_ouput])

    with gr.Tab("Hacker News 热点话题"):
        gr.Markdown("## Hacker News 热点话题")

        model_type = gr.Radio(choices=["openai", "deepseek", "ollama"], label="模型类型",
                              info="使用 OpenAI、DeepSeek API 或 Ollama 私有化模型服务")

        model_name = gr.Dropdown(choices=["gpt-4o", "gpt-4o-mini"], label="选择模型")

        # 使用 radio 组件的值来更新 dropdown 组件的选项
        model_type.change(fn=update_model_list, inputs=model_type, outputs=model_name)

        button = gr.Button(value="生成最新热点话题", variant="primary")

        markdown_output = gr.Markdown(label="热点话题输出")
        file_output = gr.File(label="下载报告")

        button.click(fn=generate_hn_hour_topic, inputs=[model_type, model_name], outputs=[markdown_output, file_output])

demo.launch(server_port=7860, share=True)
