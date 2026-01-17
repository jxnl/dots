## Goal
- Keep agent prompts and skills lean, reproducible, and context-aware.

## Repo
- This repo holds my dotfiles, shared agent prompts/skills, and install scripts for local tools.

## Installation
- Use `./install.sh` to install dotfiles (vim/bash/tmux) plus Claude/Codex/Cursor prompts.
- Use `./agents/install.sh` to install only agent prompts/skills (no dotfiles).
- Use `./install.sh --agents` to install shared prompts into Claude, Codex, and Cursor.
- Use `./install.sh --agents --only-prompts name1,name2` to install specific prompts across tools.
- Optional: `brew bundle --file Brewfile` on macOS for common tooling.

## Shell Defaults
- `bash_profile` prefers `nvim` when available, routes `rm` to `trash` if installed, and enables `noclobber`.

## Vim Plugins
- Plugins are managed with vim-plug; use `:PlugInstall` in vim/nvim.
- Neovim config installs to `~/.config/nvim/init.vim`.
