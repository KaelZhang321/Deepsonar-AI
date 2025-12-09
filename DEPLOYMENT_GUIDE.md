# DeepSonar AI 服务器部署操作手册

## 🎯 部署概述

DeepSonar AI 是一个基于 Django + Chainlit + CrewAI 的商业分析平台，包含：
- **Django 后端**：用户管理、报告存储、API接口
- **Chainlit 界面**：AI聊天交互界面
- **CrewAI 引擎**：多智能体分析系统
- **React 前端**：用户门户界面

## 🏗️ 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx         │────│  Django Backend │────│  Chainlit UI    │
│   (80/443)      │    │  (8000)         │    │  (8001)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   PostgreSQL    │    │   AI Engine     │
                       │   (5432)        │    │ (CrewAI+ARK API)│
                       └─────────────────┘    └─────────────────┘
```

## 📋 服务器要求

### 最低配置
- **CPU**: 2核心
- **内存**: 4GB RAM
- **存储**: 20GB SSD
- **操作系统**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+

### 推荐配置
- **CPU**: 4核心
- **内存**: 8GB RAM
- **存储**: 50GB SSD
- **网络**: 100Mbps+ 带宽

## 🔧 环境准备

### 1. 系统更新
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 2. 安装基础软件
```bash
# Ubuntu/Debian
sudo apt install -y python3.11 python3.11-venv python3.11-dev
sudo apt install -y nginx postgresql postgresql-contrib
sudo apt install -y git curl wget htop
sudo apt install -y build-essential libpq-dev

# CentOS/RHEL
sudo yum install -y python3.11 python3.11-devel
sudo yum install -y nginx postgresql postgresql-server
sudo yum install -y git curl wget htop
sudo yum install -y @development-tools libpq-devel
```

### 3. Node.js (用于前端构建)
```bash
# 安装 Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

## 📂 项目部署

### 1. 创建项目目录
```bash
sudo mkdir -p /opt/deepsonar
sudo chown $USER:$USER /opt/deepsonar
cd /opt/deepsonar
```

### 2. 克隆项目代码
```bash
git clone https://github.com/your-username/Deepsonar-AI.git .
```

### 3. 创建 Python 虚拟环境
```bash
cd /opt/deepsonar
python3.11 -m venv venv
source venv/bin/activate
```

### 4. 安装 Python 依赖
```bash
pip install --upgrade pip
pip install -r requirements.txt

# 安装生产环境额外依赖
pip install gunicorn psycopg2-binary redmail
```

### 5. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
nano .env
```

**关键环境变量配置：**
```bash
# 生产环境配置
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# 数据库配置
DATABASE_URL=postgresql://deepsonar:password@localhost:5432/deepsonar_db

# 火山引擎 ARK API
ARK_API_KEY=your-ark-api-key
ARK_MODEL_ENDPOINT=your-model-endpoint

# 邮件配置
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Chainlit 配置
CHAINLIT_AUTH_SECRET=your-chainlit-secret
```

## 🗄️ 数据库设置

### 1. PostgreSQL 配置
```bash
# 启动 PostgreSQL 服务
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 创建数据库和用户
sudo -u postgres psql << EOF
CREATE DATABASE deepsonar_db;
CREATE USER deepsonar WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE deepsonar_db TO deepsonar;
\q
EOF
```

### 2. Django 数据库迁移
```bash
cd /opt/deepsonar
source venv/bin/activate

# 运行迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic --noinput
```

## 🔒 SSL 证书配置

### 1. 安装 Certbot
```bash
sudo apt install certbot python3-certbot-nginx
```

### 2. 获取 SSL 证书
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 3. 设置自动续期
```bash
sudo crontab -e
# 添加以下行：
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🌐 Nginx 配置

### 1. 创建 Nginx 配置文件
```bash
sudo nano /etc/nginx/sites-available/deepsonar
```

**Nginx 配置内容：**
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL 配置
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Django 后端
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /opt/deepsonar/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /opt/deepsonar/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Chainlit 界面
    location /chat/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # React 前端 (如果使用)
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. 启用配置
```bash
sudo ln -s /etc/nginx/sites-available/deepsonar /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

## 🚀 Systemd 服务配置

### 1. Django 后端服务
```bash
sudo nano /etc/systemd/system/deepsonar-backend.service
```

**服务配置：**
```ini
[Unit]
Description=DeepSonar Django Backend
After=network.target postgresql.service

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/deepsonar
Environment=PATH=/opt/deepsonar/venv/bin
EnvironmentFile=/opt/deepsonar/.env
ExecStart=/opt/deepsonar/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 backend.config.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Chainlit 界面服务
```bash
sudo nano /etc/systemd/system/deepsonar-chat.service
```

**服务配置：**
```ini
[Unit]
Description=DeepSonar Chainlit Chat Interface
After=network.target postgresql.service

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/deepsonar
Environment=PATH=/opt/deepsonar/venv/bin
EnvironmentFile=/opt/deepsonar/.env
ExecStart=/opt/deepsonar/venv/bin/chainlit run interface/app.py --host 127.0.0.1 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. React 前端服务 (如果需要)
```bash
sudo nano /etc/systemd/system/deepsonar-frontend.service
```

**服务配置：**
```ini
[Unit]
Description=DeepSonar React Frontend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/deepsonar/portal
Environment=NODE_ENV=production
ExecStart=/usr/bin/npm run server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. 启动所有服务
```bash
sudo systemctl daemon-reload
sudo systemctl enable deepsonar-backend deepsonar-chat deepsonar-frontend
sudo systemctl start deepsonar-backend deepsonar-chat deepsonar-frontend
```

## 🔍 服务状态检查

### 1. 检查服务状态
```bash
# 检查所有服务
sudo systemctl status deepsonar-backend deepsonar-chat deepsonar-frontend

# 检查端口占用
sudo netstat -tlnp | grep -E ':800[01]'

# 检查日志
sudo journalctl -u deepsonar-backend -f
sudo journalctl -u deepsonar-chat -f
```

### 2. 测试服务可用性
```bash
# 测试 Django 后端
curl http://127.0.0.1:8000/api/health

# 测试 Chainlit 界面
curl http://127.0.0.1:8001
```

## 🔧 维护和监控

### 1. 日志管理
```bash
# Django 日志位置
tail -f /opt/deepsonar/logs/django.log

# Nginx 访问日志
tail -f /var/log/nginx/access.log

# Nginx 错误日志
tail -f /var/log/nginx/error.log
```

### 2. 数据库备份
```bash
# 创建备份脚本
sudo nano /opt/deepsonar/scripts/backup.sh
```

**备份脚本内容：**
```bash
#!/bin/bash
BACKUP_DIR="/opt/deepsonar/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 数据库备份
pg_dump -h localhost -U deepsonar deepsonar_db > $BACKUP_DIR/db_backup_$DATE.sql

# 压缩备份
gzip $BACKUP_DIR/db_backup_$DATE.sql

# 删除 7 天前的备份
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
```

```bash
# 设置执行权限
sudo chmod +x /opt/deepsonar/scripts/backup.sh

# 设置定时备份 (每天凌晨 2 点)
sudo crontab -e
# 添加：
0 2 * * * /opt/deepsonar/scripts/backup.sh
```

### 3. 系统监控
```bash
# 安装监控工具
sudo apt install htop iotop nethogs

# 监控系统资源
htop
iotop
nethogs
```

## 🚨 故障排除

### 常见问题及解决方案

#### 1. Django 服务无法启动
```bash
# 检查配置文件
python manage.py check

# 检查数据库连接
python manage.py dbshell

# 检查静态文件
python manage.py collectstatic --noinput
```

#### 2. Chainlit 界面无法访问
```bash
# 检查端口占用
sudo netstat -tlnp | grep 8001

# 重启服务
sudo systemctl restart deepsonar-chat

# 查看详细日志
sudo journalctl -u deepsonar-chat -n 50
```

#### 3. AI 引擎报错
```bash
# 检查 API 密钥
curl -H "Authorization: Bearer your-api-key" https://ark.cn-beijing.volces.com/api/v3/models

# 测试 CrewAI 功能
cd /opt/deepsonar
python -c "from ai_engine.crew import BusinessAnalysisCrew; print('AI Engine OK')"
```

#### 4. 数据库连接问题
```bash
# 检查 PostgreSQL 状态
sudo systemctl status postgresql

# 测试数据库连接
psql -h localhost -U deepsonar -d deepsonar_db -c "SELECT version();"
```

## 📈 性能优化

### 1. Django 优化
```bash
# 在 settings.py 中添加
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# 安装 Redis
sudo apt install redis-server
sudo systemctl enable redis-server
```

### 2. 数据库优化
```bash
# PostgreSQL 配置优化
sudo nano /etc/postgresql/13/main/postgresql.conf
```

**优化参数：**
```ini
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
```

### 3. Nginx 优化
```nginx
# 在 nginx 配置中添加
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

client_max_body_size 10M;
client_body_timeout 60s;
client_header_timeout 60s;
```

## 🔄 更新部署

### 1. 应用更新流程
```bash
#!/bin/bash
# /opt/deepsonar/scripts/update.sh

cd /opt/deepsonar

# 备份当前版本
sudo cp -r /opt/deepsonar /opt/deepsonar_backup_$(date +%Y%m%d_%H%M%S)

# 拉取最新代码
git pull origin main

# 更新依赖
source venv/bin/activate
pip install -r requirements.txt

# 运行数据库迁移
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

# 重启服务
sudo systemctl restart deepsonar-backend deepsonar-chat

echo "部署完成！"
```

## 🔐 安全建议

### 1. 防火墙配置
```bash
# 启用 UFW
sudo ufw enable

# 允许必要端口
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# 拒绝其他端口
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### 2. 定期安全更新
```bash
# 设置自动安全更新
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. 日志监控
```bash
# 监控异常访问
sudo tail -f /var/log/nginx/access.log | grep -E "(404|500|403)"

# 监控系统登录
sudo tail -f /var/log/auth.log | grep -E "(Failed|Invalid)"
```

## 📞 技术支持

### 关键联系人
- **系统管理员**: [联系方式]
- **开发团队**: [联系方式]
- **运维团队**: [联系方式]

### 紧急响应流程
1. **服务中断**: 立即检查系统状态和服务日志
2. **数据库问题**: 启动备份恢复程序
3. **安全问题**: 立即断开外网连接，进行安全审计

---

*本文档基于 DeepSonar AI 项目架构编写，更新日期：2025-12-09*