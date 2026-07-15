/** 记录页推荐板块与占位条目（后续可接后端） */
export interface RecordsSection {
  id: string
}

export interface RecordsItem {
  id: string
  sectionId: string
  /** i18n key suffix under records.items.* */
  titleKey: string
  summaryKey: string
  contentKey: string
  date?: string
}

export const recordsSections: RecordsSection[] = [
  { id: 'all' },
  { id: 'daily' },
  { id: 'process' },
  { id: 'travel' },
  { id: 'thoughts' },
]

export const recordsItems: RecordsItem[] = [
  {
    id: 'placeholder-daily-1',
    sectionId: 'daily',
    titleKey: 'daily_1_title',
    summaryKey: 'daily_1_summary',
    contentKey: 'daily_1_content',
    date: '2026-07-01',
  },
  {
    id: 'placeholder-process-1',
    sectionId: 'process',
    titleKey: 'process_1_title',
    summaryKey: 'process_1_summary',
    contentKey: 'process_1_content',
    date: '2026-06-20',
  },
  {
    id: 'placeholder-thoughts-1',
    sectionId: 'thoughts',
    titleKey: 'thoughts_1_title',
    summaryKey: 'thoughts_1_summary',
    contentKey: 'thoughts_1_content',
    date: '2026-06-08',
  },
]

export function recordMatchesSection(item: RecordsItem, sectionId: string): boolean {
  if (sectionId === 'all') return true
  return item.sectionId === sectionId
}
