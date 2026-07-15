export type LangCode = 'ja' | 'zh' | 'en'
export type ProjectSize = 'small' | 'medium' | 'large' | 'featured'

export interface Project {
  id: number
  slug: string
  title: string
  description: string
  cover_url: string
  tech_stack: string[]
  demo_url: string | null
  repo_url: string | null
  size: ProjectSize
  sort_order: number
  created_at: string
}

export interface KnowledgeListItem {
  id: number
  slug: string
  title: string
  summary: string
  category: string
  tags: string[]
  cover_url: string | null
  published_at: string | null
  created_at: string
}

export interface KnowledgeArticle extends KnowledgeListItem {
  content: string
}

export interface ProjectAdmin {
  id: number
  slug: string
  title_ja: string
  title_zh: string
  title_en: string
  desc_ja: string
  desc_zh: string
  desc_en: string
  cover_url: string
  tech_stack: string[]
  demo_url: string | null
  repo_url: string | null
  size: ProjectSize
  sort_order: number
  is_published: boolean
  created_at: string
}

export interface KnowledgeAdmin {
  id: number
  slug: string
  title_ja: string
  title_zh: string
  title_en: string
  summary_ja: string
  summary_zh: string
  summary_en: string
  content_ja: string
  content_zh: string
  content_en: string
  category: string
  tags: string[]
  cover_url: string | null
  is_published: boolean
  published_at: string | null
  created_at: string
}

export interface DashboardStats {
  projects_total: number
  projects_published: number
  knowledge_total: number
  knowledge_published: number
}

export interface LoginResponse {
  access_token: string
  token_type: string
}
