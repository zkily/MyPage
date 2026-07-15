/** 作品页左侧推荐板块 */
export interface ProjectSection {
  id: string
  /** 匹配 tech_stack；空表示不限技术 */
  match: string[]
  /** 可选：按 size 过滤 */
  sizes?: Array<'small' | 'medium' | 'large' | 'featured'>
}

export const projectSections: ProjectSection[] = [
  { id: 'all', match: [] },
  { id: 'featured', match: [], sizes: ['featured', 'large'] },
  {
    id: 'web',
    match: ['vue', 'react', 'typescript', 'javascript', 'tailwind', 'css', 'html', 'next'],
  },
  {
    id: 'backend',
    match: ['fastapi', 'python', 'node', 'mysql', 'postgres', 'api'],
  },
  {
    id: 'tool',
    match: ['cli', 'docker', 'tool', 'widget', 'utility'],
  },
  {
    id: 'experiment',
    match: ['experiment', 'demo', 'prototype', 'css', 'canvas'],
  },
]

export function projectMatchesSection(
  project: { tech_stack: string[]; size: string },
  section: ProjectSection,
): boolean {
  if (section.id === 'all') return true

  if (section.sizes?.length && !section.sizes.includes(project.size as 'small' | 'medium' | 'large' | 'featured')) {
    return false
  }

  if (!section.match.length) return true

  const haystack = (project.tech_stack || []).join(' ').toLowerCase()
  return section.match.some((keyword) => haystack.includes(keyword.toLowerCase()))
}
