# Tabs

Horizontal tab navigation with active indicator, keyboard navigation, and optional icons.

## Usage

```tsx
import { Tabs } from '@berunda/design-system';
import type { Tab } from '@berunda/design-system/components/Tabs/Tabs';

function Example() {
  const tabs: Tab[] = [
    {
      id: 'overview',
      label: 'Overview',
      icon: <BarChart3 size={16} />,
      content: <p>Overview content</p>,
    },
    {
      id: 'details',
      label: 'Details',
      content: <p>Details content</p>,
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: <Settings size={16} />,
      content: <p>Settings content</p>,
    },
  ];

  return (
    <Tabs
      tabs={tabs}
      defaultTabId="overview"
      onChange={(tabId) => console.log('Tab changed:', tabId)}
      aria-label="Main navigation"
    />
  );
}
```

## Props

| Prop          | Type                    | Default    | Description              |
|---------------|-------------------------|------------|--------------------------|
| tabs          | `Tab[]`                 | —          | Tab definitions          |
| defaultTabId  | `string`                | First tab  | Initially active tab     |
| onChange      | `(tabId: string) => void` | —        | Tab change callback      |
| className     | `string`                | —          | Additional CSS classes   |
| aria-label    | `string`                | `'Tabs'`   | Accessibility label      |
