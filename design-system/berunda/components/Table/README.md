# Table

A sortable, accessible data table with loading, empty, and pagination states.

## Usage

```tsx
import { Table } from '@berunda/design-system';
import type { Column } from '@berunda/design-system/components/Table/Table';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

const columns: Column<User>[] = [
  { key: 'name', header: 'Name', sortable: true },
  { key: 'email', header: 'Email', sortable: true },
  { key: 'role', header: 'Role', sortable: true },
];

function Example() {
  const data: User[] = [
    { id: 1, name: 'Alice', email: 'alice@example.com', role: 'Admin' },
    { id: 2, name: 'Bob', email: 'bob@example.com', role: 'User' },
  ];

  return (
    <Table
      columns={columns}
      data={data}
      rowKey={(row) => row.id}
      loading={false}
      emptyMessage="No users found."
      onRowClick={(row) => console.log(row)}
      pagination={<span>Showing 1–2 of 2</span>}
    />
  );
}
```

## Props

| Prop          | Type              | Default              | Description                  |
|---------------|-------------------|----------------------|------------------------------|
| columns       | `Column<T>[]`     | —                    | Column definitions           |
| data          | `T[]`             | —                    | Row data                     |
| loading       | `boolean`         | `false`              | Show loading overlay         |
| emptyMessage  | `string`          | `'No data available.'` | Empty state message        |
| pagination    | `ReactNode`       | —                    | Pagination controls slot     |
| onRowClick    | `(row: T) => void`| —                    | Row click handler            |
| rowKey        | `(row: T) => string \| number` | —         | Unique key extractor         |
| className     | `string`          | —                    | Additional CSS classes       |
