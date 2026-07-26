# LoadingSpinner

An animated loading indicator with optional label.

## Usage

```tsx
import { LoadingSpinner } from '@berunda/design-system';

function Example() {
  return (
    <>
      <LoadingSpinner size="sm" />
      <LoadingSpinner size="md" label="Loading data..." />
      <LoadingSpinner size="lg" label="Processing" />
    </>
  );
}
```

## Props

| Prop      | Type                            | Default  | Description              |
|-----------|---------------------------------|----------|--------------------------|
| size      | `'sm' \| 'md' \| 'lg'`         | `'md'`   | Spinner size             |
| label     | `string`                        | —        | Accessible label text    |
| className | `string`                        | —        | Additional CSS classes   |
