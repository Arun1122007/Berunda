# Badge

A small label for statuses, counts, and tags.

## Usage

```tsx
import { Badge } from '@berunda/design-system';

function Example() {
  return (
    <>
      <Badge variant="success" size="sm">Active</Badge>
      <Badge variant="warning">Pending</Badge>
      <Badge variant="error">Failed</Badge>
      <Badge variant="info">12 new</Badge>
      <Badge variant="default">Draft</Badge>
    </>
  );
}
```

## Props

| Prop     | Type                                                              | Default     | Description          |
|----------|-------------------------------------------------------------------|-------------|----------------------|
| variant  | `'default' \| 'success' \| 'warning' \| 'error' \| 'info'`       | `'default'` | Color variant        |
| size     | `'sm' \| 'md'`                                                    | `'md'`      | Badge size           |
| children | `React.ReactNode`                                                 | —           | Badge content        |
| className| `string`                                                          | —           | Additional CSS classes|
