---
name: powerpoint
description: >-
  Create, read, and edit PowerPoint (.pptx) decks — extract text, edit templates,
  or build slides from scratch. Use when the user mentions slides, deck,
  presentation, .pptx, or invokes /powerpoint_*.
disable-model-invocation: true
---

# powerpoint

## When to use

Use whenever a `.pptx` is involved (create, read, edit, split, merge, notes, templates). Trigger phrases: "make a deck", "edit slides", "pitch deck", `.pptx`, `/powerpoint_*`.

## Working directory

Prefer (in order):

| Target | Path |
|--------|------|
| **Canonical (after `/ai-pro-skills` clone)** | `~/.ai-pro-skills/powerpoint` |
| **Cursor** (full tree install) | `~/.cursor/skills/powerpoint` |
| **Hermes all profiles** | `~/.hermes/skills/productivity/powerpoint` |
| **Hermes this profile** | `${HERMES_HOME}/skills/productivity/powerpoint` |

Always `cd` into the working directory before running skill scripts. Guides in this folder: `editing.md`, `pptxgenjs.md`.

## Slash commands

| Slash | CLI / action | Description |
|-------|--------------|-------------|
| `/powerpoint_read` | `python -m markitdown FILE.pptx` | Extract text from deck |
| `/powerpoint_unpack` | `unzip -o FILE.pptx -d unpacked/` | Extract PPTX as ZIP/XML |
| `/powerpoint_add-slide` | `python scripts/add_slide.py unpacked/ slideN.xml` | Duplicate slide or create from layout |
| `/powerpoint_clean` | `python scripts/clean.py unpacked/` | Remove orphaned slides/media |
| `/powerpoint_pack` | `python scripts/office/pack.py unpacked/ out.pptx [--original FILE.pptx]` | Repack + validate |
| `/powerpoint_create` | Follow `pptxgenjs.md` (`npx pptxgenjs` / Node) | Create deck from scratch |
| `/powerpoint_edit` | Follow `editing.md` | Template-based edit workflow |
| `/powerpoint_to-pdf` | `soffice --headless --convert-to pdf FILE.pptx` | Convert to PDF (LibreOffice) |
| `/powerpoint_to-images` | `pdftoppm -jpeg -r 150 FILE.pdf slide` | PDF → slide images for QA |

## How to run

1. `cd` to the [working directory](#working-directory) that exists on this machine.
2. Pick a workflow:

### Read

```bash
python -m markitdown presentation.pptx
```

### Edit existing / template

1. Read content (`markitdown`) and plan layouts (see `editing.md`).
2. Unpack: `unzip -o template.pptx -d unpacked/`
3. Structural edits: `python scripts/add_slide.py …`, edit `unpacked/ppt/slides/slide*.xml`, reorder `presentation.xml`.
4. `python scripts/clean.py unpacked/`
5. `python scripts/office/pack.py unpacked/ output.pptx --original template.pptx`

### Create from scratch

Follow **`pptxgenjs.md`** in this folder (`npm` / `pptxgenjs`). Prefer bold, topic-specific design — avoid plain white + bullets.

### Visual QA

```bash
soffice --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Inspect `slide-*.jpg` for overflow, overlap, low contrast, leftover placeholders (`xxxx`, `lorem`). Fix and re-verify at least once.

## Notes

- Bundled scripts present here: `scripts/add_slide.py`, `scripts/clean.py`, `scripts/office/pack.py` (+ helpers/schemas).
- Do **not** call missing upstream helpers (`thumbnail.py`, `office/unpack.py`, `office/soffice.py`) — use `unzip`, system `soffice`, and `pdftoppm` instead.
- Deps: `pip install "markitdown[pptx]"`; `npm i -g pptxgenjs` (create); LibreOffice + Poppler (QA images).
- License: see `LICENSE.txt` in this folder.
