import { useState, useCallback } from 'react';
import clsx from 'clsx';
import styles from './Tabs.module.css';

export interface Tab {
  id: string;
  label: string;
  content: React.ReactNode;
  icon?: React.ReactNode;
}

interface TabsProps {
  tabs: Tab[];
  defaultTabId?: string;
  onChange?: (tabId: string) => void;
  className?: string;
  'aria-label'?: string;
}

export default function Tabs({
  tabs,
  defaultTabId,
  onChange,
  className,
  'aria-label': ariaLabel = 'Tabs',
}: TabsProps) {
  const [activeId, setActiveId] = useState(
    defaultTabId || (tabs.length > 0 ? tabs[0].id : undefined),
  );

  const handleTabClick = useCallback(
    (tabId: string) => {
      setActiveId(tabId);
      onChange?.(tabId);
    },
    [onChange],
  );

  if (tabs.length === 0) return null;

  const activeTab = tabs.find((t) => t.id === activeId);

  return (
    <div className={clsx(styles.tabs, className)} data-testid="tabs">
      <div
        role="tablist"
        aria-label={ariaLabel}
        className={styles.tabList}
      >
        {tabs.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={tab.id === activeId}
            aria-controls={`tabpanel-${tab.id}`}
            tabIndex={tab.id === activeId ? 0 : -1}
            className={clsx(styles.tab, tab.id === activeId && styles.tabActive)}
            onClick={() => handleTabClick(tab.id)}
            onKeyDown={(e) => {
              const idx = tabs.findIndex((t) => t.id === tab.id);
              let nextIdx: number | null = null;
              if (e.key === 'ArrowRight') nextIdx = (idx + 1) % tabs.length;
              if (e.key === 'ArrowLeft') nextIdx = (idx - 1 + tabs.length) % tabs.length;
              if (nextIdx !== null) {
                e.preventDefault();
                handleTabClick(tabs[nextIdx].id);
                document.getElementById(`tab-${tabs[nextIdx].id}`)?.focus();
              }
            }}
            data-testid={`tab-${tab.id}`}
          >
            {tab.icon && <span className={styles.tabIcon}>{tab.icon}</span>}
            {tab.label}
          </button>
        ))}
      </div>
      {activeTab && (
        <div
          role="tabpanel"
          id={`tabpanel-${activeTab.id}`}
          aria-labelledby={`tab-${activeTab.id}`}
          tabIndex={0}
          className={styles.tabPanel}
          data-testid={`tabpanel-${activeTab.id}`}
        >
          {activeTab.content}
        </div>
      )}
    </div>
  );
}
