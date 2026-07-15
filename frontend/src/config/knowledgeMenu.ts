/** 知识页左侧推荐板块；新增板块时在此追加，并补全 i18n */
export interface KnowledgeSection {
  id: string
  /** 用于匹配文章 category / tags（大小写不敏感） */
  match: string[]
}

export const knowledgeSections: KnowledgeSection[] = [
  { id: 'all', match: [] },
  {
    id: 'frontend',
    match: ['フロントエンド', '前端', 'frontend', 'vue', 'react', 'typescript', 'css'],
  },
  {
    id: 'backend',
    match: ['バックエンド', '后端', 'backend', 'fastapi', 'python', 'api', 'mysql'],
  },
  {
    id: 'design',
    match: ['デザイン', '设计', 'design', 'ui', 'ux', 'typography'],
  },
  {
    id: 'tools',
    match: ['ツール', '工具', 'tools', 'git', 'docker', 'linux'],
  },
  {
    id: 'reading',
    match: ['読書', '阅读', 'reading', 'book', '笔记'],
  },
]

export function articleMatchesSection(
  article: { category: string; tags: string[] },
  section: KnowledgeSection,
): boolean {
  if (section.id === 'all' || section.match.length === 0) return true
  const haystack = [article.category, ...(article.tags || [])]
    .join(' ')
    .toLowerCase()
  return section.match.some((keyword) => haystack.includes(keyword.toLowerCase()))
}
