# Getting Started with Slidev

Get started with Slidev presentations in minutes.

## Run a Presentation

```bash
cd slides
bun run dev              # Default "reference" deck
bun run dev -- <deck-name>  # Specific deck
```

Visit `http://localhost:3030` (or port shown in terminal).

## Basic Slide Structure

Slides are separated by `---`:

```markdown
---
# Frontmatter (optional)
---

# Slide Title

Content goes here.

---

# Next Slide

More content.
```

## Deployment

### Build a Single Deck

```bash
cd slides

# Build outputs to decks/<deck-name>/dist/<deck-name>/
bun run slidev build decks/<deck-name>/slides.md --base /<deck-name>/ --out dist/<deck-name>
```

Note: The build output goes to `decks/<deck-name>/dist/<deck-name>/`, not `dist/<deck-name>/`.

### Deploy a Single Deck

```bash
cd slides

# Build the deck
bun run slidev build decks/<deck-name>/slides.md --base /<deck-name>/ --out dist/<deck-name>

# Copy to main dist directory
cp -r decks/<deck-name>/dist/<deck-name> dist/

# Deploy to Cloudflare Pages
bunx wrangler pages deploy dist --project-name presentations
```

Your deck will be available at `https://<deployment-id>.presentations-1yj.pages.dev/<deck-name>/`

### Build and Deploy All Decks

```bash
cd slides

# Build all decks and deploy
./deploy.sh
```

This runs `build-all.sh` which:
- Builds every deck in `decks/` that has a `slides.md`
- Creates an index page listing all decks
- Sets up Cloudflare Pages routing
- Deploys to Cloudflare Pages

## Next Steps

- **Creating slides?** → See [BASICS.md](./BASICS.md)
- **New presentation?** → See [DRAFTING.md](./DRAFTING.md)
- **Adding animations?** → See [POLISHING.md](./POLISHING.md)

