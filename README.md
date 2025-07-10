# Vim User Manual

## Installation

1. **Install Vundle** (Vim plugin manager):
   ```sh
   git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
   ```
2. **Clone this repo** and copy the files:
   ```sh
   cp vimrc ~/.vimrc
   cp -r colors ~/.vim/
   ```
3. **Install plugins**: Open Vim and run:
   ```vim
   :BundleInstall
   ```

## Key Features & Plugins

### General
- **Colorscheme:** molokai
- **Syntax highlighting** and 256-color support
- **No scrollbars or arrow keys** (hardcore mode)
- **Tabs as 4 spaces** (auto/smart indent, expandtab)
- **Auto-read files on change**
- **No backup or swap files**
- **Persistent undo**
- **Wildmenu/wildmode** for command completion
- **Line numbers, ruler, and match highlighting**

### Keybindings
- `ww` — Fast save
- `:W` — Sudo save (write as root)
- `<Space>` — Search (`/`)
- `<C-Space>` — Backward search (`?`)
- `wj`, `wk`, `wh`, `wl` — Move between windows (splits)
- `<S-Tab>` — Indent left (`<<`)
- `\f` — Fuzzy find file in current buffer dir
- `\m` — Fuzzy find file from full cwd
- `\d` — Open NERDTree (directory tree)
- `\u` — Toggle Gundo (undo history)

### Plugins
- **Vundle** — Plugin manager
- **vim-airline** — Status/tabline
- **vim-fugitive** — Git integration
- **vim-easymotion** — Fast cursor movement
- **nerdcommenter** — Easy code commenting
- **NERDTree & NERDTree-tabs** — File explorer
- **Gundo** — Visual undo tree
- **Syntastic** — Syntax checking (now using Ruff for Python)
- **delimitMate** — Auto-close quotes, brackets, etc.
- **vim-snippets** — Snippet support
- **minibufexpl, mru, FuzzyFinder, L9** — Buffer/file navigation
- **vim-markdown** — Markdown enhancements
- **python-syntax** — Enhanced Python highlighting
- **vim-latex** — LaTeX support

### Python
- **Linting:** Uses Ruff via Syntastic. Make sure `ruff` is installed in your environment:
  ```sh
  uv pip install ruff
  ```
  Syntastic will automatically use Ruff for Python files.
- **Trailing whitespace:** Automatically removed on save for `.py` files.
- **80-column marker:** Shown for Python files.

### Markdown
- Spell check enabled
- Line numbers disabled

### CSS
- Tab width set to 2
- Wrap at 79th character

### Miscellaneous
- **No backup/swap files**
- **Persistent undo** (stored in `~/.vim/undo`)
- **Wildignore:** Ignores `.o`, `.obj`, `.git`, `.pyc` files in completion

## Tips
- Use `:NERDTree` or `\d` to open the file explorer
- Use `\u` to toggle the undo tree
- Use `ww` to save quickly
- Use `:W` to save with sudo if you get a permission error
- Use `wj`, `wk`, `wh`, `wl` to move between splits
- Use FuzzyFinder (`\f`, `\m`) for fast file navigation

## Zsh & Oh-My-Zsh
- Install zsh and oh-my-zsh for a better shell experience:
  ```sh
  brew install zsh
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
  ```
  See https://sourabhbajaj.com/mac-setup/iTerm/zsh.html for more details.

## tmux User Guide

tmux is a terminal multiplexer: it lets you run and manage multiple terminal sessions in one window. This is great for multitasking, remote work, and keeping persistent sessions.

### Basic Usage
- Start tmux: `tmux`
- Detach: `Ctrl-b d` (leaves session running in background)
- List sessions: `tmux ls`
- Attach to session: `tmux attach -t <session-name>`
- Kill session: `tmux kill-session -t <session-name>`

### Your Custom Keybindings (from .tmux.conf)
- **Prefix:** `Ctrl-b` (default), but also `Ctrl-a` (Screen-style)
- **Reload config:** `prefix r` (e.g., `Ctrl-b r`)
- **Split pane horizontally:** `prefix -`
- **Split pane vertically:** `prefix _`
- **Move between panes:** `prefix h/j/k/l`
- **Resize panes:** `prefix H/J/K/L` (shifted)
- **Swap panes:** `prefix >` (down), `prefix <` (up)
- **Create new window:** `prefix c`
- **Next/prev window:** `prefix Ctrl-l` (next), `prefix Ctrl-h` (prev)
- **Last window:** `prefix Tab`
- **Maximize pane:** `prefix +`
- **Show undo history:** Not available in tmux, but see Vim's Gundo
- **Clear screen/history:** `Ctrl-l` (clears both)

### Tips
- Use `prefix` + `Enter` to enter copy mode (scrollback, copy text)
- Use `prefix U` to view URLs in the current pane
- Use `prefix F` to run Facebook PathPicker (if installed)
- Mouse support can be toggled with `prefix m`
- For more, see your `.tmux.conf` or run `man tmux`

## bash_profile User Guide

Your `bash_profile` customizes your shell environment and command-line experience. Here’s what it does:

### Prompt Customization
- Sets a custom prompt (`PS1`) to show the current directory, host, user, and a new line with `>>>`.
- Sets a secondary prompt (`PS2`) for multi-line commands.

### Color Support
- Enables colored output for commands like `ls` by setting `CLICOLOR=1` and a custom `LSCOLORS` scheme.

### Safer and More Convenient Aliases
- `rm` is disabled by default (prints a warning). Use `/bin/rm` or the `remove` alias for actual deletion.
- `remove` prompts before deleting recursively and verbosely.
- `cp` and `mv` prompt before overwriting and show what’s happening.
- `mkdir` creates parent directories as needed and shows what’s created.
- `cd..`, `..`, `...` are shortcuts to go up 1 or 2 directory levels.
- `~` quickly jumps to your home directory.
- `c` clears the terminal screen.

### Directory Listing
- `lr` gives a full recursive directory listing in a tree-like format, piped through `less` for easy viewing.

### Sourcing
- `bashrc` is an alias to source your `~/.bash_profile` (reloads your shell config).

---

## Credits
- Some inspiration from https://github.com/amix/vimrc/blob/master/vimrcs/extended.vim

---

This user manual covers all major features, plugins, and keybindings in your Vim configuration. For plugin-specific help, see the plugin documentation or use `:help <plugin>` in Vim.

