/** 前台导航：新增板块时在此追加一项，并注册对应路由即可 */
export interface SiteNavItem {
  name: string
  path: string
  labelKey: string
}

export const siteNav: SiteNavItem[] = [
  { name: 'about', path: '/about', labelKey: 'nav.about' },
  { name: 'projects', path: '/projects', labelKey: 'nav.projects' },
  { name: 'records', path: '/records', labelKey: 'nav.records' },
  { name: 'knowledge', path: '/knowledge', labelKey: 'nav.knowledge' },
  { name: 'contact', path: '/contact', labelKey: 'nav.contact' },
]
