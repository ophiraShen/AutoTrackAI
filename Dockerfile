# Dockerfile

# 使用官方的 python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目的所有文件到容器
COPY . .

# 复制并执行 validate_test.sh 脚本
COPY validate_test.sh .
RUN chmod +x validate_test.sh
RUN ./validate_test.sh

# 设置容器入口
CMD ["python", "src/daemon_process.py"]