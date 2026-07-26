# Modal

A dialog component with overlay, header, body, footer, and close button. Uses React Portal and includes focus trapping, Escape key handling, and animations.

## Usage

```tsx
import { useState } from 'react';
import { Modal, Button } from '@berunda/design-system';

function Example() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setOpen(true)}>Open Modal</Button>
      <Modal
        isOpen={open}
        onClose={() => setOpen(false)}
        title="Confirm Action"
        size="md"
        footerContent={
          <>
            <Button variant="ghost" onClick={() => setOpen(false)}>Cancel</Button>
            <Button variant="primary" onClick={() => setOpen(false)}>Confirm</Button>
          </>
        }
      >
        <p>Are you sure you want to proceed?</p>
      </Modal>
    </>
  );
}
```

## Props

| Prop          | Type                                            | Default   | Description               |
|--------------|-------------------------------------------------|-----------|---------------------------|
| isOpen       | `boolean`                                       | —         | Show/hide modal           |
| onClose      | `() => void`                                    | —         | Close handler             |
| title        | `string`                                        | —         | Modal title               |
| size         | `'sm' \| 'md' \| 'lg' \| 'fullscreen'`         | `'md'`    | Modal width               |
| children     | `React.ReactNode`                               | —         | Modal body content        |
| footerContent| `React.ReactNode`                               | —         | Content for footer area   |
