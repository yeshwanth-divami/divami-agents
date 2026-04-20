---
name: lit-parse
description: Parse PDFs, Office docs, and images into readable text files with the local `lit` CLI, including batch conversion patterns and filename normalization guidance.
---

# lit-parse

`lit` is a Node.js CLI for parsing documents locally — no API key required.

## Installation

```bash
npm install -g @llamaindex/lit
```

Binary: `/Users/yeshwanth/.nvm/versions/node/v22.16.0/bin/lit`

## Commands

### Single file
```bash
lit parse <file> -o <output> --format text -q
```

### Batch (same format for all)
```bash
lit batch-parse <input-dir> <output-dir> --format text --extension .docx -q
```

## Key Options

| Flag | Default | Notes |
|------|---------|-------|
| `--format` | `text` | `text` or `json` (no native markdown) |
| `--no-ocr` | off | Skip OCR for text-native docs |
| `-q` | off | Suppress progress output |
| `--extension` | all | Filter by extension in batch mode |
| `--recursive` | off | Recurse subdirs in batch mode |

## Output format note

`lit` outputs **plain text**, not markdown. Save with `.md` extension when the user wants markdown files — the content will be text but readable as markdown.

## Kebab-case filename conversion (shell)

```bash
parse() {
  lit parse "$DIR/$1" -o "$DIR/docs/$2" --format text -q
}

parse "My File Name.docx" "my-file-name.md"
```

Rules for kebab-case:
- Lowercase everything
- Replace spaces, underscores, special chars (`(`, `)`, `-`) with `-`
- Collapse multiple `-` into one
- Strip leading/trailing `-`

## Supported file types

PDF, DOCX, XLSX, PPTX, images (PNG, JPG, etc.)
