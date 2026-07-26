# Card

A flexible card container with variants and sub-components.

## Usage

```tsx
import { Card, CardHeader, CardBody, CardFooter } from '@berunda/design-system';

function Example() {
  return (
    <Card variant="elevated" padding="lg">
      <CardHeader>
        <h3>Card Title</h3>
      </CardHeader>
      <CardBody>
        <p>Main content goes here.</p>
      </CardBody>
      <CardFooter>
        <Button variant="primary">Action</Button>
      </CardFooter>
    </Card>
  );
}
```

## Props

### Card

| Prop     | Type                                                        | Default     | Description                |
|----------|-------------------------------------------------------------|-------------|----------------------------|
| variant  | `'default' \| 'elevated' \| 'outlined' \| 'interactive'`   | `'default'` | Visual style              |
| padding  | `'none' \| 'sm' \| 'md' \| 'lg'`                           | `'md'`      | Inner padding             |
| onClick  | `() => void`                                                | —           | Makes card interactive     |
| className| `string`                                                    | —           | Additional CSS classes     |

### CardHeader, CardBody, CardFooter

| Prop     | Type              | Description            |
|----------|-------------------|------------------------|
| children | `React.ReactNode` | Content               |
| className| `string`          | Additional CSS classes |
