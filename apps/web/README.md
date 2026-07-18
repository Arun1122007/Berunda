# @berunda/web — Berunda Crime Intelligence Platform

React single-page application for the Berunda Crime Intelligence Platform.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | React 18 |
| Language | TypeScript (strict) |
| Build | Vite 5 |
| Styling | Tailwind CSS 3 |
| Routing | React Router v6 |
| Maps | MapLibre GL JS |
| Graphs | Cytoscape.js |
| Charts | Recharts |
| Icons | Lucide React |
| Testing | Vitest + Testing Library |

## Prerequisites

- Node.js >= 18
- npm >= 9

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start Vite dev server with HMR |
| `npm run build` | Type-check and build for production |
| `npm run preview` | Preview production build locally |
| `npm run test` | Run test suite with Vitest |
| `npm run lint` | Lint source files with ESLint |
| `npm run typecheck` | Run TypeScript type checking |

## Project Structure

```
src/
├── app/                  # App root (router, error boundary)
│   ├── App.tsx
│   └── App.css
├── styles/               # Global styles and CSS variables
│   └── globals.css
├── types/                # TypeScript type definitions
│   ├── api.ts            # API request/response types
│   ├── domain.ts         # Domain model types
│   └── index.ts          # Re-exports
├── services/             # API client and auth services
│   ├── api-client.ts     # HTTP client with interceptors
│   └── auth.ts           # Authentication service
├── hooks/                # Custom React hooks
│   ├── useAuth.ts
│   └── useApi.ts
├── components/
│   ├── ui/               # Reusable UI primitives
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── ErrorBoundary.tsx
│   │   └── Badge.tsx
│   ├── layout/           # Layout components
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   └── Layout.tsx
│   └── shared/           # Shared components
│       └── ProtectedRoute.tsx
└── features/             # Feature modules (route-based lazy loading)
    ├── dashboard/
    ├── hotspot/
    ├── graph/
    ├── analytics/
    ├── rag/
    ├── admin/
    └── auth/
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `/api` | Base URL for Catalyst Functions API |

## Development

The app uses React.lazy and Suspense for code splitting. Each feature module is loaded on demand via route-based splitting. Tailwind CSS classes follow the Berunda design system with custom color tokens defined in `tailwind.config.js`.
