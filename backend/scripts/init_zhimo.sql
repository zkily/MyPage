-- 知墨 (zhimo) 数据库初始化
-- 推荐库名：zhimo（与站点品牌一致，ASCII 安全）
-- 用法（在 PowerShell）：
--   & "C:\Program Files\MySQL\MySQL Server 9.2\bin\mysql.exe" -u root -p < backend/scripts/init_zhimo.sql

CREATE DATABASE IF NOT EXISTS zhimo
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'zhimo'@'localhost' IDENTIFIED BY 'zhimo123';
CREATE USER IF NOT EXISTS 'zhimo'@'%' IDENTIFIED BY 'zhimo123';
GRANT ALL PRIVILEGES ON zhimo.* TO 'zhimo'@'localhost';
GRANT ALL PRIVILEGES ON zhimo.* TO 'zhimo'@'%';
FLUSH PRIVILEGES;

USE zhimo;

-- 管理员
CREATE TABLE IF NOT EXISTS admin_users (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(64) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_admin_users_username (username),
  KEY ix_admin_users_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 作品
CREATE TABLE IF NOT EXISTS projects (
  id INT NOT NULL AUTO_INCREMENT,
  slug VARCHAR(128) NOT NULL,
  title_ja VARCHAR(255) NOT NULL,
  title_zh VARCHAR(255) NOT NULL DEFAULT '',
  title_en VARCHAR(255) NOT NULL DEFAULT '',
  desc_ja TEXT NOT NULL,
  desc_zh TEXT NOT NULL,
  desc_en TEXT NOT NULL,
  cover_url VARCHAR(512) NOT NULL DEFAULT '',
  tech_stack JSON NOT NULL,
  demo_url VARCHAR(512) NULL,
  repo_url VARCHAR(512) NULL,
  size ENUM('small', 'medium', 'large', 'featured') NOT NULL DEFAULT 'medium',
  sort_order INT NOT NULL DEFAULT 0,
  is_published TINYINT(1) NOT NULL DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_projects_slug (slug),
  KEY ix_projects_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 知识 / 笔记文章
CREATE TABLE IF NOT EXISTS knowledge_articles (
  id INT NOT NULL AUTO_INCREMENT,
  slug VARCHAR(128) NOT NULL,
  title_ja VARCHAR(255) NOT NULL,
  title_zh VARCHAR(255) NOT NULL DEFAULT '',
  title_en VARCHAR(255) NOT NULL DEFAULT '',
  summary_ja TEXT NOT NULL,
  summary_zh TEXT NOT NULL,
  summary_en TEXT NOT NULL,
  content_ja TEXT NOT NULL,
  content_zh TEXT NOT NULL,
  content_en TEXT NOT NULL,
  category VARCHAR(64) NOT NULL DEFAULT '',
  tags JSON NOT NULL,
  cover_url VARCHAR(512) NULL,
  is_published TINYINT(1) NOT NULL DEFAULT 0,
  published_at DATETIME NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_knowledge_articles_slug (slug),
  KEY ix_knowledge_articles_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
