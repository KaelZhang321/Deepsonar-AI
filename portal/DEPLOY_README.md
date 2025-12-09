# DeepSonar 服务器部署指南

本文档详细说明了如何将 DeepSonar 项目部署到服务器。我们要将前端 (Vite/React) 和后端 (Node/Express) 打包为一个 Docker 镜像统一运行。

## 1. 部署架构

- **前端**: React + Vite (构建为静态文件)
- **后端**: Node.js + Express (提供 API 并在生产环境托管前端静态文件)
- **容器化**: Docker (多阶段构建)

## 2. 环境要求

服务器需要安装：
- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/)

## 3. 快速部署 (使用脚本)

项目根目录下提供了一个 `deploy.sh` 脚本，可一键完成构建和启动。

1. **上传/克隆代码到服务器**
   ```bash
   git clone <your-repo-url> deepsonar
   cd deepsonar
   ```

2. **添加执行权限**
   ```bash
   chmod +x deploy.sh
   ```

3. **运行部署脚本**
   ```bash
   ./deploy.sh
   ```
   该脚本会执行以下操作：
   - 构建 Docker 镜像 (`deepsonar-app`)
   - 停止并删除旧容器 (如果存在)
   - 启动新容器，映射端口 `3001`

4. **访问应用**
   打开浏览器访问: `http://<服务器IP>:3001`

## 4. 手动部署 (Docker)

如果不使用脚本，可以使用以下命令手动部署：

### 构建镜像
```bash
docker build -t deepsonar-app .
```

### 运行容器
```bash
docker run -d \
  --name deepsonar-app \
  -p 3001:3001 \
  --restart unless-stopped \
  deepsonar-app
```

## 5. 环境变量配置

如果需要配置 SMTP 邮件服务或其他环境变量，可以在运行 Docker 时通过 `-e` 参数传入，或使用 `.env` 文件。

### 方式 A: 命令行参数
```bash
docker run -d \
  --name deepsonar-app \
  -p 3001:3001 \
  -e SMTP_HOST=smtp.example.com \
  -e SMTP_USER=user@example.com \
  -e SMTP_PASS=secret \
  deepsonar-app
```

### 方式 B: 使用 .env 文件 (推荐)
1. 在服务器项目根目录创建 `.env` 文件：
   ```env
   SMTP_HOST=smtp.example.com
   SMTP_PORT=587
   SMTP_USER=user@example.com
   SMTP_PASS=your_password
   # CONTACT_EMAIL=admin@example.com
   ```

2. 启动时挂载或读取文件：
   ```bash
   docker run -d \
     --name deepsonar-app \
     -p 3001:3001 \
     --env-file .env \
     deepsonar-app
   ```

## 6. 开发环境说明

在本地开发时：

1. **安装依赖**
   ```bash
   npm install
   cd server && npm install
   ```

2. **启动后端** (端口 3001)
   ```bash
   cd server
   npm start
   ```

3. **启动前端** (端口 3000)
   ```bash
   # 在项目根目录
   npm run dev
   ```
   *注意：前端配置了代理，访问 `/api` 会自动转发到 `localhost:3001`。*

## 7. 常见问题排查

- **无法访问页面？**
  - 检查服务器防火墙是否开放 3001 端口。
  - 使用 `docker logs deepsonar-app` 查看服务日志。

- **邮件发送失败？**
  - 检查 SMTP 环境变量是否正确配置。
  - 查看容器日志中的错误信息。

- **如何更新代码？**
  - 执行 `git pull` 拉取最新代码。
  - 再次运行 `./deploy.sh` 重新构建并重启。
