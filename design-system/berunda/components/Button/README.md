# Button

A versatile button component with multiple variants, sizes, and states.

## Usage

```tsx
import { Button } from '@berunda/design-system';

function Example() {
  return (
    <>
      <Button variant="primary" onClick={() => alert('Clicked!')}>
        Primary
      </Button>
      <Button variant="secondary" size="lg" loading>
        Loading
      </Button>
      <Button variant="outline" icon={<ArrowRight />} iconPosition="right">
        Next
      </Button>
      <Button variant="ghost" fullWidth>
        Full Width
      </Button>
      <Button variant="danger" disabled>
        Disabled
      </Button>
    </>
  );
}
```

## Props

| Prop         | Type                                          | Default     | Description                |
|-------------|-----------------------------------------------|-------------|----------------------------|
| variant     | `'primary' \| 'secondary' \| 'outline' \| 'ghost' \| 'danger'` | `'primary'` | Visual style            |
| size        | `'sm' \| 'md' \| 'lg'`                        | `'md'`      | Button size               |
| loading     | `boolean`                                     | `false`     | Show loading spinner       |
| disabled    | `boolean`                                     | `false`     | Disabled state             |
| icon        | `React.ReactNode`                             | —           | Icon element               |
| iconPosition| `'left' \| 'right'`                           | `'left'`    | Icon placement             |
| fullWidth   | `boolean`                                     | `false`     | Stretch to container width |
| type        | `'button' \| 'submit' \| 'reset'`             | `'button'`  | Button type attribute      |
