# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **React + Vite** expense tracker starter project. It's intentionally built with bugs, poor UI, and messy code as a teaching tool for a Claude Code course.

## Commands

```bash
# Install dependencies
npm install

# Start development server (runs on http://localhost:5173)
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Preview production build
npm run preview
```

## Architecture

### Tech Stack
- **React 19** (with hooks)
- **Vite 7** as build tool
- **ESLint 9** with flat config
- No TypeScript, no testing framework

### Project Structure
```
src/
├── App.jsx       # Main component - all logic lives here (state, handlers, render)
├── App.css       # Component styles
├── main.jsx      # Entry point - mounts App in StrictMode
└── index.css     # Global reset + base styles
```

### Key Code Patterns (App.jsx)

**State management**: All state in a single `App` component using `useState`:
- `transactions` - array of transaction objects
- Form fields: `description`, `amount`, `type`, `category`
- Filters: `filterType`, `filterCategory`

**Transaction shape**:
```js
{ id, description, amount, type: "income"|"expense", category, date }
```

**Known issues** (per README):
- Bug in income/expense calculation (amounts stored as strings)
- Poor UI
- Messy code - all in one component

## Linting

ESLint flat config in `eslint.config.js`:
- Ignores `dist/`
- Recommended React hooks + React refresh rules
- Treats unused vars as errors (except UPPER_CASE constants)
- Runs on `**/*.{js,jsx}`

Run with: `npm run lint`