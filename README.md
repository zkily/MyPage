# 知墨 — 个人主页

Vue 3 + FastAPI + MySQL 全栈个人作品集与知识分享站点。

## 功能

- 前台：知墨品牌，质朴水墨风；多页面（关于 / 作品 / 记录 / 知识 / 联系）
- 三语切换：日语（默认）/ 中文 / English
- 后台 CMS：作品与知识文章的增删改查、图片上传、三语内容编辑

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3, Vite, TypeScript, Tailwind CSS, Pinia, vue-i18n |
| 后端 | FastAPI, SQLAlchemy, Alembic |
| 数据库 | MySQL 8 |

## 快速启动

### 1. 启动 MySQL

需要已安装 Docker，或使用本地 MySQL 8 实例。

```bash
docker compose up -d
```

若使用本地 MySQL，请创建数据库 `zhimo` 和用户，并修改 `backend/.env` 中的 `DATABASE_URL`。
可执行：`mysql -u root -p < backend/scripts/init_zhimo.sql`

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API 文档：http://localhost:8000/docs

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

- 前台：http://localhost:5173
- 后台：http://localhost:5173/admin

### 默认管理员账号

- 用户名：`admin`
- 密码：`admin123`

可在 `backend/.env` 中修改。

## 环境变量

复制 `backend/.env.example` 为 `backend/.env` 并按需修改：

- `DATABASE_URL` — MySQL 连接串（默认库名 `zhimo`）
- `JWT_SECRET` — JWT 签名密钥
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` — 初始管理员（仅首次 seed 时生效）

## 项目结构

```
知墨/
├── frontend/     # Vue 3 前台 + Admin CMS
├── backend/      # FastAPI API
├── docker-compose.yml
└── README.md
```

## 部署提示

生产环境建议：

1. 修改 `JWT_SECRET` 和管理员密码
2. 使用 Nginx 反向代理前端静态文件与 `/api`、`/static`
3. MySQL 使用独立实例并配置备份
