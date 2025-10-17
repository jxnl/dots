# Dots Directory

Personal dotfiles repository for development tools and environments.

## Contents

- **vimrc** - Vim configuration with plugins and keybindings
- **tmux.conf** - Tmux terminal multiplexer configuration  
- **bash_profile** - Bash shell configuration
- **colors/** - Vim color schemes
- **claude/** - Claude AI assistant configuration and command documentation

## Installation

1. Install Vundle:
   ```bash
   git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
   ```

2. Install dotfiles:
   ```bash
   git clone https://github.com/jxnl/dots.git
   cd dots
   chmod +x install.sh
   ./install.sh                    # Install all components
   ./install.sh --claude           # Install only Claude config
   ./install.sh --vim              # Install only vim config
   ./install.sh --bash             # Install only bash config
   ./install.sh --tmux             # Install only tmux config
   ./install.sh --help             # Show all options
   ```

3. Install Vim plugins:
   ```bash
   vim +BundleInstall +qall
   ```

## Installation Flags

The installer supports selective installation with these flags:

- `--vim` - Install only vim configuration (vimrc + colors)
- `--bash` - Install only bash configuration (bash_profile)
- `--tmux` - Install only tmux configuration (tmux.conf)
- `--claude` - Install only Claude configuration (claude/)
- `--help` - Show usage information and all available flags

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