# Manus Credit Manager 部署指南

本文档详细介绍了如何在不同环境中部署 Manus Credit Manager 应用程序。

## 目录

1. [部署概述](#部署概述)
2. [环境要求](#环境要求)
3. [本地开发部署](#本地开发部署)
4. [生产环境部署](#生产环境部署)
5. [Docker 部署](#docker-部署)
6. [云平台部署](#云平台部署)
7. [配置说明](#配置说明)
8. [监控和维护](#监控和维护)
9. [故障排除](#故障排除)

## 部署概述

Manus Credit Manager 是一个基于 Flask 的 Web 应用程序，具有以下特点：

- **轻量级架构**：使用 SQLite 数据库，无需复杂的数据库配置
- **自包含设计**：前端和后端集成在同一个应用中
- **跨平台支持**：支持 Linux、Windows、macOS 等操作系统
- **容器化友好**：支持 Docker 容器化部署

### 应用组件

1. **Flask Web 服务器**：处理 HTTP 请求和 API 调用
2. **SQLite 数据库**：存储用户数据和账户信息
3. **静态文件服务**：提供前端 HTML、CSS、JavaScript 文件
4. **后台任务调度器**：执行定时积分获取任务
5. **Selenium WebDriver**：实现 Web 自动化操作

## 环境要求

### 基础要求

- **Python 版本**：3.8 或更高版本
- **内存要求**：最少 512MB RAM，推荐 1GB 或更多
- **存储空间**：最少 100MB 可用空间
- **网络连接**：稳定的互联网连接

### 系统依赖

**Linux 系统：**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip
```

**Windows 系统：**
- 从 [Python 官网](https://www.python.org/) 下载并安装 Python 3.8+
- 确保在安装时勾选"Add Python to PATH"选项

**macOS 系统：**
```bash
# 使用 Homebrew
brew install python3

# 或使用官方安装包
# 从 Python 官网下载 macOS 安装包
```

### 浏览器要求

由于应用使用 Selenium 进行 Web 自动化，需要安装支持的浏览器：

- **Chrome**：推荐使用，兼容性最好
- **Firefox**：备选方案
- **Edge**：Windows 环境下的选择

## 本地开发部署

### 快速开始

1. **获取源代码**
```bash
# 如果使用 Git
git clone <repository-url>
cd manus-credit-manager

# 或者下载并解压源代码包
```

2. **创建虚拟环境**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **初始化数据库**
```bash
# 数据库会在首次运行时自动创建
# 无需手动初始化
```

5. **启动应用**
```bash
python src/main.py
```

6. **访问应用**
- 打开浏览器访问：http://localhost:5000
- 应用将在本地 5000 端口运行

### 开发环境配置

**环境变量设置：**
```bash
# Linux/macOS
export FLASK_ENV=development
export FLASK_DEBUG=1
export SECRET_KEY=your-development-secret-key

# Windows
set FLASK_ENV=development
set FLASK_DEBUG=1
set SECRET_KEY=your-development-secret-key
```

**调试模式启动：**
```bash
# 启用调试模式
FLASK_ENV=development python src/main.py
```

调试模式特性：
- 代码更改时自动重启
- 详细的错误信息显示
- 交互式调试器

## 生产环境部署

### 使用 Gunicorn（推荐）

Gunicorn 是一个高性能的 WSGI HTTP 服务器，适合生产环境：

1. **安装 Gunicorn**
```bash
pip install gunicorn
```

2. **创建 WSGI 入口文件**
```python
# wsgi.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app

if __name__ == "__main__":
    app.run()
```

3. **启动 Gunicorn**
```bash
# 基本启动
gunicorn --bind 0.0.0.0:5000 wsgi:app

# 生产环境配置
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --timeout 120 \
         --keep-alive 2 \
         --max-requests 1000 \
         --max-requests-jitter 100 \
         wsgi:app
```

### 使用 uWSGI

uWSGI 是另一个优秀的应用服务器选择：

1. **安装 uWSGI**
```bash
pip install uwsgi
```

2. **创建配置文件**
```ini
# uwsgi.ini
[uwsgi]
module = wsgi:app
master = true
processes = 4
socket = /tmp/manus-credit-manager.sock
chmod-socket = 666
vacuum = true
die-on-term = true
```

3. **启动 uWSGI**
```bash
uwsgi --ini uwsgi.ini
```

### 反向代理配置

#### Nginx 配置

```nginx
# /etc/nginx/sites-available/manus-credit-manager
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件直接服务
    location /static {
        alias /path/to/manus-credit-manager/src/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/manus-credit-manager /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Apache 配置

```apache
# /etc/apache2/sites-available/manus-credit-manager.conf
<VirtualHost *:80>
    ServerName your-domain.com
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
    
    # 静态文件直接服务
    Alias /static /path/to/manus-credit-manager/src/static
    <Directory "/path/to/manus-credit-manager/src/static">
        Require all granted
    </Directory>
</VirtualHost>
```

### 系统服务配置

创建 systemd 服务文件：

```ini
# /etc/systemd/system/manus-credit-manager.service
[Unit]
Description=Manus Credit Manager
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/manus-credit-manager
Environment=PATH=/path/to/manus-credit-manager/venv/bin
Environment=FLASK_ENV=production
Environment=SECRET_KEY=your-production-secret-key
ExecStart=/path/to/manus-credit-manager/venv/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启用和启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable manus-credit-manager
sudo systemctl start manus-credit-manager
sudo systemctl status manus-credit-manager
```

## Docker 部署

### 创建 Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Chrome 浏览器
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 安装 ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    && chmod +x /usr/local/bin/chromedriver

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录
RUN mkdir -p /app/data

# 设置环境变量
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "src.main:app"]
```

### 创建 docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  manus-credit-manager:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-production-secret-key
      - SIMPLE_KEY=your-encryption-key
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - manus-credit-manager
    restart: unless-stopped
```

### 构建和运行

```bash
# 构建镜像
docker build -t manus-credit-manager .

# 使用 docker-compose 运行
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 云平台部署

### Heroku 部署

1. **准备 Heroku 配置文件**

```python
# Procfile
web: gunicorn src.main:app
```

```python
# runtime.txt
python-3.9.16
```

2. **部署步骤**
```bash
# 安装 Heroku CLI
# 登录 Heroku
heroku login

# 创建应用
heroku create your-app-name

# 设置环境变量
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key

# 部署
git push heroku main
```

### AWS EC2 部署

1. **启动 EC2 实例**
   - 选择 Ubuntu 20.04 LTS AMI
   - 配置安全组开放 80 和 443 端口

2. **连接并配置服务器**
```bash
# 连接到实例
ssh -i your-key.pem ubuntu@your-ec2-ip

# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装依赖
sudo apt install python3 python3-pip python3-venv nginx -y

# 部署应用（按照生产环境部署步骤）
```

### Google Cloud Platform 部署

1. **使用 App Engine**

```yaml
# app.yaml
runtime: python39

env_variables:
  FLASK_ENV: production
  SECRET_KEY: your-secret-key

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

2. **部署命令**
```bash
gcloud app deploy
```

## 配置说明

### 环境变量

| 变量名 | 描述 | 默认值 | 必需 |
|--------|------|--------|------|
| FLASK_ENV | Flask 运行环境 | development | 否 |
| SECRET_KEY | Flask 密钥 | 随机生成 | 生产环境必需 |
| SIMPLE_KEY | 加密密钥 | demo_key_12345 | 否 |
| DATABASE_URL | 数据库连接字符串 | sqlite:///app.db | 否 |

### 应用配置

**生产环境建议配置：**

```python
# config.py
import os

class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
```

### 数据库配置

**SQLite（默认）：**
- 适合小型部署和开发环境
- 无需额外配置
- 数据文件位于 `src/database/app.db`

**PostgreSQL（推荐生产环境）：**
```python
# 安装依赖
pip install psycopg2-binary

# 配置连接
DATABASE_URL = 'postgresql://username:password@localhost/dbname'
```

**MySQL：**
```python
# 安装依赖
pip install PyMySQL

# 配置连接
DATABASE_URL = 'mysql+pymysql://username:password@localhost/dbname'
```

## 监控和维护

### 日志配置

```python
# logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    if not app.debug:
        file_handler = RotatingFileHandler(
            'logs/manus-credit-manager.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
```

### 健康检查

应用提供了健康检查端点：

```bash
# 检查应用状态
curl http://your-domain.com/api/health

# 预期响应
{
  "status": "healthy",
  "message": "Manus Credit Manager is running"
}
```

### 性能监控

**使用 Prometheus 和 Grafana：**

1. **安装 prometheus_flask_exporter**
```bash
pip install prometheus_flask_exporter
```

2. **配置监控**
```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)
```

### 备份策略

**数据库备份：**
```bash
# SQLite 备份
cp src/database/app.db backups/app_$(date +%Y%m%d_%H%M%S).db

# 自动备份脚本
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DB_FILE="/path/to/app.db"
DATE=$(date +%Y%m%d_%H%M%S)

cp $DB_FILE $BACKUP_DIR/app_$DATE.db

# 保留最近 30 天的备份
find $BACKUP_DIR -name "app_*.db" -mtime +30 -delete
```

**配置定时备份：**
```bash
# 添加到 crontab
0 2 * * * /path/to/backup_script.sh
```

## 故障排除

### 常见问题

**问题 1：应用无法启动**

```bash
# 检查 Python 版本
python3 --version

# 检查依赖安装
pip list

# 查看详细错误
python src/main.py
```

**问题 2：数据库连接失败**

```bash
# 检查数据库文件权限
ls -la src/database/

# 检查磁盘空间
df -h

# 重新创建数据库
rm src/database/app.db
python src/main.py
```

**问题 3：Selenium 自动化失败**

```bash
# 检查 Chrome 安装
google-chrome --version

# 检查 ChromeDriver
chromedriver --version

# 测试 Selenium
python -c "from selenium import webdriver; driver = webdriver.Chrome(); driver.quit()"
```

### 调试技巧

**启用详细日志：**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**使用 Flask 调试模式：**
```bash
FLASK_ENV=development FLASK_DEBUG=1 python src/main.py
```

**检查网络连接：**
```bash
# 测试外部连接
curl -I https://manus.im

# 检查端口占用
netstat -tlnp | grep 5000
```

### 性能优化

**数据库优化：**
```sql
-- 创建索引
CREATE INDEX idx_user_username ON user(username);
CREATE INDEX idx_manus_account_email ON manus_account(email);
CREATE INDEX idx_credit_history_date ON credit_history(date);
```

**应用优化：**
```python
# 使用连接池
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

---

**文档版本：** 1.0.0  
**最后更新：** 2025年6月23日  
**维护团队：** Manus AI 开发团队

