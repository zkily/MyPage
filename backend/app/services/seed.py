from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.models.models import AdminUser, KnowledgeArticle, Project, ProjectSize


def seed_database(db: Session) -> None:
    settings = get_settings()

    if not db.query(AdminUser).filter(AdminUser.username == settings.admin_username).first():
        db.add(
            AdminUser(
                username=settings.admin_username,
                password_hash=get_password_hash(settings.admin_password),
            )
        )

    if db.query(Project).count() == 0:
        db.add_all(
            [
                Project(
                    slug="personal-portfolio",
                    title_ja="パーソナルポートフォリオ",
                    title_zh="个人作品集",
                    title_en="Personal Portfolio",
                    desc_ja="Vue 3 と FastAPI で構築したモダンなポートフォリオサイト。",
                    desc_zh="使用 Vue 3 与 FastAPI 构建的现代化作品集网站。",
                    desc_en="A modern portfolio site built with Vue 3 and FastAPI.",
                    cover_url="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800",
                    tech_stack=["Vue 3", "FastAPI", "MySQL", "Tailwind CSS"],
                    demo_url="http://localhost:5173",
                    repo_url="https://github.com",
                    size=ProjectSize.featured,
                    sort_order=1,
                    is_published=True,
                ),
                Project(
                    slug="task-manager",
                    title_ja="タスク管理アプリ",
                    title_zh="任务管理应用",
                    title_en="Task Manager App",
                    desc_ja="リアルタイム同期に対応した軽量タスク管理ツール。",
                    desc_zh="支持实时同步的轻量任务管理工具。",
                    desc_en="A lightweight task manager with real-time sync.",
                    cover_url="https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800",
                    tech_stack=["React", "Node.js", "PostgreSQL"],
                    demo_url=None,
                    repo_url="https://github.com",
                    size=ProjectSize.medium,
                    sort_order=2,
                    is_published=True,
                ),
                Project(
                    slug="weather-widget",
                    title_ja="天気ウィジェット",
                    title_zh="天气小组件",
                    title_en="Weather Widget",
                    desc_ja="美しい UI の天気表示ウィジェット。",
                    desc_zh="界面精美的天气展示小组件。",
                    desc_en="A beautiful weather display widget.",
                    cover_url="https://images.unsplash.com/photo-1592210454359-9043f067919b?w=800",
                    tech_stack=["TypeScript", "CSS"],
                    size=ProjectSize.small,
                    sort_order=3,
                    is_published=True,
                ),
            ]
        )

    if db.query(KnowledgeArticle).count() == 0:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        db.add_all(
            [
                KnowledgeArticle(
                    slug="vue3-composition-api",
                    title_ja="Vue 3 Composition API 入門",
                    title_zh="Vue 3 Composition API 入门",
                    title_en="Getting Started with Vue 3 Composition API",
                    summary_ja="Composition API の基本と実践的な使い方を解説します。",
                    summary_zh="讲解 Composition API 的基础与实践用法。",
                    summary_en="An introduction to Composition API basics and practical usage.",
                    content_ja="## はじめに\n\nComposition API は Vue 3 の核心機能です。\n\n```js\nimport { ref } from 'vue'\nconst count = ref(0)\n```",
                    content_zh="## 简介\n\nComposition API 是 Vue 3 的核心特性。\n\n```js\nimport { ref } from 'vue'\nconst count = ref(0)\n```",
                    content_en="## Introduction\n\nComposition API is a core feature of Vue 3.\n\n```js\nimport { ref } from 'vue'\nconst count = ref(0)\n```",
                    category="フロントエンド",
                    tags=["Vue", "JavaScript", "Frontend"],
                    is_published=True,
                    published_at=now,
                ),
                KnowledgeArticle(
                    slug="fastapi-best-practices",
                    title_ja="FastAPI ベストプラクティス",
                    title_zh="FastAPI 最佳实践",
                    title_en="FastAPI Best Practices",
                    summary_ja="スケーラブルな API 設計のための実践ガイド。",
                    summary_zh="可扩展 API 设计的实践指南。",
                    summary_en="A practical guide to scalable API design.",
                    content_ja="## アーキテクチャ\n\nルーター、サービス、モデルを分離しましょう。",
                    content_zh="## 架构\n\n将路由、服务与模型分层组织。",
                    content_en="## Architecture\n\nSeparate routers, services, and models.",
                    category="バックエンド",
                    tags=["Python", "FastAPI", "Backend"],
                    is_published=True,
                    published_at=now,
                ),
            ]
        )

    db.commit()
