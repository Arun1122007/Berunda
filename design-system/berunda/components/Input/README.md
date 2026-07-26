# Input

Form input component with label, error, helper text, and icon support. Supports both `<input>` and `<textarea>` via the `textarea` prop.

## Usage

```tsx
import { Input, InputLabel, InputHelperText, InputErrorMessage } from '@berunda/design-system';

function Example() {
  return (
    <>
      <Input
        label="Email"
        type="email"
        placeholder="you@example.com"
        helperText="We'll never share your email."
      />

      <Input
        label="Password"
        type="password"
        error="Password must be at least 8 characters."
        leftIcon={<Lock />}
      />

      <Input
        textarea
        label="Description"
        placeholder="Enter details..."
        rows={4}
      />
    </>
  );
}
```

## Props

| Prop       | Type                                                        | Default   | Description                  |
|-----------|-------------------------------------------------------------|-----------|------------------------------|
| label     | `string`                                                    | —         | Input label text             |
| error     | `string`                                                    | —         | Error message                |
| helperText| `string`                                                    | —         | Helper text below input      |
| leftIcon  | `React.ReactNode`                                           | —         | Icon on left side            |
| rightIcon | `React.ReactNode`                                           | —         | Icon on right side           |
| fullWidth | `boolean`                                                   | `true`    | Stretch to container width   |
| textarea  | `boolean`                                                   | `false`   | Render as textarea           |
| disabled  | `boolean`                                                   | `false`   | Disabled state               |
| readOnly  | `boolean`                                                   | `false`   | Read-only state              |
