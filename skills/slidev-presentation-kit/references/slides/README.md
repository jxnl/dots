# Welcome to [Slidev](https://github.com/slidevjs/slidev)!

This is a presentation starter kit with a deck-based structure.

## Getting Started

To start the slide show:

- `bun install`
- `bun run dev` - Opens the default "reference" deck
- `bun run dev -- <deck-name>` - Opens a specific deck (e.g., `bun run dev -- reference`)
- visit <http://localhost:3030>

## Deck Structure

Presentations are organized in the `slides/decks/` directory. Each deck is a folder containing:
- `slides.md` - The main slide content file
- `pages/` - (Optional) Additional slide files that can be imported

The default "reference" deck is located at `slides/decks/reference/` and contains example slides.

To create a new deck:
1. Create a new directory under `slides/decks/` (e.g., `slides/decks/my-presentation/`)
2. Add a `slides.md` file in that directory
3. Run `bun run dev -- my-presentation`

Edit the slides in `slides/decks/<deck-name>/slides.md` to see the changes.

Learn more about Slidev at the [documentation](https://sli.dev/).
