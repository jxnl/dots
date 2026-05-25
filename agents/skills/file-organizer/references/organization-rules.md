# File Organization Rules

## Default Workflow

- Build a plan before mutating files.
- Default to new/changed files since the last run; do a full audit when requested.
- Store Markdown logs and lightweight state in `/Users/jasonliu/Downloads/.cleanup_logs`.
- Write each run log with proposed/applied moves, renames, syncs, duplicates, assumptions, and unresolved items.

## Naming

- Use precise compact `snake_case`.
- Prefer the date visible in the document.
- If no document date is clear, use download/modified date and note the assumption.
- Avoid full account numbers. Use partial IDs like `x190`, `3684`, or last4 when needed.
- Remove Finder/browser duplicate suffixes like `(1)` or `(2)` when renaming.
- Use short descriptive suffixes for conflicts, such as `_v2`, `_alternate`, or a source-specific suffix.

Examples:

- `paystub_567studio_2025-12-31.pdf`
- `bank_statement_mercury_3684_2025-05.pdf`
- `statement_schwab_x190_2025-05.pdf`
- `investment_summary_schwab_x190_2024.pdf`
- `event_sfo_jfk_flight_2026-02-10.ics`

## Permanent Documents Taxonomy

Use `/Users/jasonliu/Documents` as the local source of truth. Preserve the existing top-level style:

- `Finance`
- `Investments`
- `Legal_Documents`
- `Work_Documents`
- `Travel_Documents`
- `Books`
- `Course_Materials`
- `Reference`
- `Media`

Finance conventions:

- Tax folders use `YYYY_Tax`, for example `Documents/Finance/2025_Tax`.
- Bank files go under `Documents/Finance/Bank_{institution}`.
- Brokerage files go under `Documents/Finance/Brokerage_{account}` or `Brokerage_misc`.
- Paystubs go under `Documents/Finance/Paystubs_{employer}`.
- Receipts go under `Documents/Finance/Receipts`.
- Retirement files go under `Documents/Finance/Retirement`.
- Transaction exports go under `Documents/Finance/Transactions_{source}`.
- Tax workspaces from extracted zips stay under `Documents/Finance/YYYY_Tax/{package_name}` until filing is complete.

Investment conventions:

- Investment deal folders use company slugs, for example `Documents/Investments/kalshi`.
- Group overview, memo, subscription agreement, SPV agreement, and deal wire instructions by deal.
- Keep personal bank/wire details only in `Finance/Bank_*`, never in deal folders.

Documents conventions:

- Contracts, NDAs, signed agreements: `Documents/Contracts` unless formal legal, then `Legal_Documents`.
- Offer letters and employment docs: `Work_Documents`.
- IDs: `Documents/IDs`.
- Insurance: `Documents/Insurance`.
- Medical: `Documents/Medical`.
- Presentations: `Documents/Presentations`.
- Misc durable references: `Documents/Reference`.

Travel conventions:

- One folder per trip under `Travel_Documents/{city_YYYY-MM}`.
- Put itineraries, boarding passes, reservations, and trip ICS files in that trip folder.

## Desktop Rules

- Optimize for a nearly empty Desktop.
- Leave useful intentional aliases and symlinks in place.
- Use only these minimal bins when items should not move directly to permanent storage:
  - `Active`
  - `Desktop_Review`
  - `Screenshots`
  - `Recordings`
- Move durable screenshots to `Documents/Media/Screenshots/YYYY-MM`.
- Move durable recordings to `Documents/Media/Recordings/YYYY-MM`.
- Treat media as important only when it appears tied to work, product demos, finance, legal, travel, or active projects.

## Downloads Rules

- Classify top-level files and folders.
- Inspect PDFs/images only when filenames or surrounding folders are ambiguous.
- For existing folders, inspect top-level contents, summarize purpose, then propose moving/renaming the folder as a unit.
- Put code or project bundles in `/Users/jasonliu/dev/_incoming_review`, not Documents.
- Put installers, DMGs, PKGs, extracted app bundles, and obsolete zips into review/deletion proposals; do not sync them.
- Plan archive extraction only when contents matter. Keep or delete original archives only after confirmation.

## Google Drive Mirror

- Google Drive is a mirror, not the primary source of truth.
- Mirror only important durable documents:
  - legal
  - finance
  - tax
  - bank and brokerage statements
  - IDs
  - medical
  - insurance
  - investments
  - contracts
  - work/employment docs
  - travel itineraries
  - durable learning materials
- Do not mirror installers, junk, app caches, casual screenshots, casual recordings, or temporary media.
- Mirror the `Documents/...` path structure into Google Drive.
- If no local Google Drive root is found, stop before sync and ask Jason for the exact path.
- Once a Drive root is available and the apply step is confirmed, create missing mirror directories as needed.

Common locations to check:

- `/Users/jasonliu/Library/CloudStorage`
- `/Volumes`
- Any user-provided Google Drive path

## Duplicates, Conflicts, And Deletes

- Do not overwrite.
- If the destination exists, compare contents when feasible.
- If files are byte-identical, mark as duplicate.
- If files differ, keep both with a descriptive suffix.
- Use conservative reporting for exact duplicates, old installers, extracted zips, and obvious junk.
- Do not trash or delete without explicit confirmation.

## Logs And State

- Log directory: `/Users/jasonliu/Downloads/.cleanup_logs`.
- Include:
  - timestamp
  - source folders inspected
  - proposed and applied actions
  - rename assumptions
  - sync status
  - duplicates and delete-review candidates
  - unresolved questions
- Keep lightweight last-run state in the same directory so future runs can default to new/changed files.
