# AGENTS.md

Project-specific guidance for agents working in this repository. The global
rules in `~/.agents/AGENTS.md` also apply. This file only adds repo-specific
knowledge, so read both before starting.

## What this is

A Quartz v5 fork that publishes an Obsidian vault as a static site at
`https://riberoc.github.io/vault`. The site uses a custom color theme, a hero
banner plugin, and several Quartz community plugins.

## Layout

- `content/`: Markdown notes. **Generated** by `sync-with-vault.py`, which wipes
  and repopulates the folder from the local Obsidian vault (`~/diamond`). Do not
  hand-edit; the next sync discards the changes.
- `quartz/`: Quartz framework source (components, plugins, CLI, styles).
- `.quartz/plugins/`: Installed third-party plugins. Gitignored, recreated by
  `npx quartz plugin install`.
- `quartz.config.yaml`: Site config: title, base URL, theme colors, plugin list.
- `quartz/styles/custom.scss`: Site-specific CSS. See "Theming".
- `docs/`: Quartz's own upstream docs. The preview workflows build this, not
  `content/`.
- `index.html`: Root redirect to `/vault/about-me`, copied to the deploy root.
- `public/`: Build output. Gitignored; never edit by hand.
- `sync-with-vault.py`, `sync-and-post.py`: Content sync scripts.

## Commands

Requires Node 22 or newer. `.node-version` pins v22.16.0 and `.npmrc` sets
`engine-strict=true`.

- `npm install` then `npx quartz plugin install`: one-time setup.
- `npx quartz build --serve`: local preview at `http://localhost:8080/`.
- `npx quartz build --serve --baseDir /vault`: mirrors the production prefix.
- `npm run check`: TypeScript and Prettier check.
- `npm test`: test suite (`tsx --test`).
- `python3 sync-and-post.py`: sync the vault into `content/`, then run
  `npx quartz sync` against upstream.

`baseUrl` is `riberoc.github.io/vault`, so generated absolute URLs include the
`/vault` prefix. Pass `--baseDir /vault` when you need production-like routing.

## Content workflow

`sync-and-post.py` calls `sync-with-vault.py`, which:

1. Deletes `content/`.
2. Walks the vault at `DEFAULT_VAULT_DIR = "~/diamond"`.
3. Keeps only notes tagged `publish`.
4. Copies linked assets and strips quotes from `cover:` frontmatter.

Change those defaults in `sync-with-vault.py` if the vault moves.

## Deployment

- Pushing to `v5` triggers `.github/workflows/deploy-v5.yaml`, which builds with
  `npx quartz build -d content -v` and deploys to GitHub Pages.
- The workflow mounts the site under `/vault`: it moves everything into
  `public/vault/` except `CNAME` and `404.html`, then copies `index.html` to
  `public/index.html`.
- Keep `404.html` at the artifact root. GitHub Pages only reads a root `404.html`.
- Keep a generated `index.html` inside `public/vault/`, otherwise `/vault` 404s.
  Do not add `! -name index.html` to the move step.
- Most workflows only run when `github.repository == 'riberoc/website'`. The
  `origin` remote is `git@github.com:riberoc/website.git`, so they do run here.

## Theming

- Colors live in `quartz.config.yaml` under `configuration.theme.colors`, split
  into `lightMode` and `darkMode`. Quartz turns them into CSS variables
  (`--light`, `--secondary`, `--textHighlight`, and so on) under `:root` and
  `:root[saved-theme="dark"]`.
- `quartz/styles/custom.scss` is emitted **outside** the `@layer quartz-base`
  wrapper, so its rules win over the generated variables. Use it for overrides
  and extra CSS.
- Syntax highlighting colors come from the `syntax-highlighting` plugin's
  `theme.light` and `theme.dark` options (shiki theme names), not from CSS
  variables.
- The `alias-redirects` plugin emits case-preserving redirect stubs such as
  `public/About-me.html`. They are regenerated on every build, not stale; do not
  delete them.

## Conventions

- Python: follow `~/.agents/PYTHON_STYLES.md`.
- Prose and Markdown: follow `~/.agents/WRITING.md` (no em-dashes).
- Do not commit `public/`, `node_modules/`, or `.quartz-cache/`. All are
  gitignored.
- `README.md` is intentionally empty in this fork.
