# src/hacker_news_client.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import os
from logger import LOG

class HackerNewsClient:
    def __init__(self):
        self.url = 'https://news.ycombinator.com/'  # Hacker News的URL
    
    def fetch_top_stories(self):
        LOG.debug("准备获取 Hacker News 的热门话题")
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            top_stories = self.parse_stories(response.text)
            return top_stories
        except Exception as e:
            LOG.error(f"获取 Hacker News 的热门话题失败: {e}")
            return [] 
        
    def parse_stories(self, html_content):
        LOG.debug("准备解析 Hacker News 的热门话题")
        soup = BeautifulSoup(html_content, 'html.parser')
        stories = soup.find_all('tr', class_='athing')

        top_stories = []
        for story in stories:
            title_tag = story.find('span', class_='titleline').find('a')
            if title_tag:
                title = title_tag.text
                link = title_tag['href']
                top_stories.append({'title': title, 'link': link})

        LOG.info(f"成功解析 {len(top_stories)} 个热门话题")
        return top_stories
    
    def export_top_stories(self, date=None, hour=None):
        LOG.debug("准备导出热门话题")
        top_stories = self.fetch_top_stories()

        if not top_stories:
            LOG.warning("没有找到热门话题，跳过导出")
            return
        
        # 如果未提供 date 和 hour 参数，使用当前日期和时间
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        if hour is None:
            hour = datetime.now().strftime('%H')

        # 构建存储路径
        dir_path = os.path.join('hacker_news', date)
        os.makedirs(dir_path, exist_ok=True)

        file_path = os.path.join(dir_path, f'{hour}.md')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# Hacker News Top Stories ({date} {hour}:00)\n\n")
            for idx, story in enumerate(top_stories, start=1):
                f.write(f"{idx}. [{story['title']}]({story['link']})\n")

        LOG.info(f"成功导出热门话题到 {file_path}")
        return file_path
    

if __name__ == "__main__":
    client = HackerNewsClient()
    client.export_top_stories(date="2024-09-01", hour="14")

