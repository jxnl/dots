# Dots Directory

Personal dotfiles repository for development tools and environments.

## Contents

- **vimrc** - Vim configuration with plugins and keybindings
- **tmux.conf** - Tmux terminal multiplexer configuration  
- **bash_profile** - Bash shell configuration
- **colors/** - Vim color schemes
- **agents/** - Shared agent prompts + tool-specific settings (including Codex skills)

## Codex Commands

Custom slash commands for Codex CLI workflows (also compatible with Claude Code and Cursor):

### GitHub Workflows
- **gh-commit** - Smart commit manager with conventional commits, branch safety
- **gh-review-pr** - Comprehensive PR review (metadata, code, CI, discussions)
- **gh-address-pr-comments** - Interactive PR comment resolution
- **gh-fix-ci** - Auto-detect and fix CI failures from logs

### Development Tools
- **make-tests** - Collaborative test creation with coverage analysis
- **de-slop** - Remove AI artifacts (redundant comments, mock-heavy tests, fake data)
- **new-cmd** - Command creation helper

### Agents
- **youtube** - YouTube transcript processing

Files:
- `agents/AGENTS.md` - Global instructions (uv, no mocking, commit conventions)

## Installation

Dependencies: bash, git, curl, vim (or neovim).

Optional: install a trash CLI so `rm` routes to the Trash (e.g. `brew install trash`).

1. Install vim-plug (optional; auto-installs on first Vim/Neovim start):
   ```bash
   curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
     https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
   ```

2. Install dotfiles:
   ```bash
   git clone https://github.com/jxnl/dots.git
   cd dots
   chmod +x install.sh
   # Codex (default)
   ./install.sh --openai          # or: ./install.sh --codex
   # All agents (Codex + Claude + Cursor)
   ./install.sh --agents
   # Claude (optional)
   ./install.sh                    # Install all components
   ./install.sh --claude           # Install only Claude config
   ./install.sh --vim              # Install only vim config
   ./install.sh --bash             # Install only bash config
   ./install.sh --tmux             # Install only tmux config
   ./install.sh --skills           # Install only Codex skills
   ./install.sh --help             # Show all options
   ```

3. Install Vim/Neovim plugins:
   ```bash
   vim +PlugInstall +qall
   # or
   nvim +PlugInstall +qall
   ```

## Installation Flags

The installer supports selective installation with these flags:

- `--interactive` - Interactive installer (prompts for choices)
- `--backup` - Backup existing destination files before overwriting
- `--dry-run` - Print actions without writing files
- `--vim` - Install only vim configuration (vimrc + colors)
- `--bash` - Install only bash configuration (bash_profile)
- `--tmux` - Install only tmux configuration (tmux.conf)
- `--agents` - Install assistant prompts (Claude + Codex + Cursor)
- `--claude` - Install only Claude configuration
- `--openai`/`--codex` - Install only Codex configuration (OpenAI Developers)
- `--cursor` - Install only Cursor commands (global)
- `--cursor-project` - Install Cursor commands to .cursor/commands (project)
- `--skills` - Install Codex skills to ~/.codex/skills
- `--prompt NAME` - Install only one prompt (repeatable)
- `--only-prompts a,b,c` - Install only these prompts (comma-separated)
- `--list-prompts` - List available prompts
- `--help` - Show usage information and all available flags

## Notes

- `gitignore` is provided as a template and is not installed automatically.
- `bash_profile` prefers `nvim` when available, routes `rm` to `trash` if installed, and enables `noclobber`.
- Vim plugins are managed with vim-plug and can be installed via `:PlugInstall`.

## Key Plugins & Shortcuts

### Navigation
- **Easymotion**: `\\w`, `\\j`, `\\k`, `\\f{char}` - Quick movement
- **NERDTree**: `\d` - File explorer
- **fzf.vim**: `\f` (files), `\g` (content), `:Buffers`, `:Commits`
- **MRU**: `\m` - Recent files
- **vim-tmux-navigator**: `Ctrl+h/j/k/l` - Navigate vim/tmux

### Editing
- **vim-surround**: `cs"'`, `ds"`, `ysiw]`, `yss)`
- **vim-gitgutter**: `]c`/`[c` (next/prev change), `<leader>hs` (stage hunk)
- **Gundo**: `\u` - Undo tree

### Tools
- **vim-fugitive**: `:Gstatus`, `:Gcommit`, `:Gblame`, `:Gdiff`
- **Syntastic**: Auto syntax checking, `:SyntasticCheck`
- **vim-airline**: Enhanced status bar with git info

### Window Management
- `Ctrl+w` + `v/s/q/o/r/=`

### Essential Commands
- `gg=G` - Auto-indent file
- `zt/zz/zb` - Position line (top/middle/bottom)
- `zo/zc/zR/zM` - Fold controls
- `:s/old/new/g` - Search/replace
- `:set list` - Show invisible chars

## Zsh Setup (Optional)

```bash
brew install zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```
