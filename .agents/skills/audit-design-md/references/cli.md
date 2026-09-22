# Official CLI Reference — `@google/design.md`

Load this reference when installing, scripting, debugging the CLI, or using
`diff`/`export` in depth. The validator is the official npm package
`@google/design.md`; this skill never reimplements it.

## Installation

```bash
# Global install (recommended when the skill is used frequently)
npm install -g @google/design.md

# Verify
designmd --version
```

### The `designmd` shim

The package's binary is named `design.md`, which collides with the Windows
Markdown file association. Use the dot-free shim for portability:

```bash
npx -p @google/design.md designmd lint DESIGN.md
```

On Windows always use the shim. On Linux/macOS both names generally work.

### Troubleshooting: `ENOVERSIONS`

This error means npm cannot reach the public registry. Check:

```bash
npm config get registry   # expect https://registry.npmjs.org/
```

## Commands

All commands accept a file path or `-` for stdin; output defaults to JSON.

### `lint`

Validate a DESIGN.md file.

```bash
designmd lint DESIGN.md
designmd lint DESIGN.md --format json   # structured findings
designmd lint -                         # read from stdin
```

**Exit codes:** `0` = no errors, `1` = errors found (warnings alone do not
fail).

Output shape:

```json
{
  "findings": [
    { "severity": "error", "path": "colors.primary", "message": "..." }
  ],
  "summary": { "errors": 0, "warnings": 2, "infos": 1 }
}
```

### `diff`

Compare two versions of a DESIGN.md.

```bash
designmd diff DESIGN.md DESIGN-v2.md
```

Reports token-level changes per section, findings before/after, and a
`regression: bool` flag.

**Exit codes:** `0` = no regressions, `1` = regressions found.

### `export`

Export tokens to a target format.

```bash
designmd export --format json-tailwind   # Tailwind v3 theme.extend
designmd export --format css-tailwind    # Tailwind v4 @theme {} (--color-*, --font-*, --radius-*, --spacing-*)
designmd export --format tailwind        # alias for json-tailwind
designmd export --format dtcg            # W3C Design Tokens Format Module
```

**Exit codes:** `0` = success, `1` = bad format, `2` = unreadable input.

### `spec`

Print the spec itself — useful for injecting spec context into agent prompts.

```bash
designmd spec                        # full spec
designmd spec --rules                # spec + lint rules table
designmd spec --rules-only           # only the rules table
designmd spec --format markdown      # human-readable; default is json
```

## Programmatic API

```ts
import { lint } from '@google/design.md/linter';
// report.findings, report.summary, report.designSystem
```

Useful if a project integrates validation into tests or CI directly rather than
shelling out.