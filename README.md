# Dots Directory

This is my personal dotfiles repository containing configuration files for various development tools and environments.

## Contents

- **vimrc** - Vim configuration with plugins and keybindings
- **tmux.conf** - Tmux terminal multiplexer configuration  
- **bash_profile** - Bash shell configuration
- **colors/** - Vim color schemes
- **claude/** - Claude AI assistant configuration and command documentation

## Installation
--------

Before anything else, make sure you install `Vundle` before using the vimrc file, otherwise you'll just get tonnes of errors and non of the magic that comes with vim.

To install Vundle:
  
    $ git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle

Some bits inspired by https://github.com/amix/vimrc/blob/master/vimrcs/extended.vim

To install the `.vimrc` file, just clone this repo and `mv /vim-files/.vimrc ~` along with the `colors` repo.
After you install `Vundle`, just run `:BundleInstall`

## Install zsh and oh-my-zsh

```
brew install zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

follow https://sourabhbajaj.com/mac-setup/iTerm/zsh.html for more details

# Plugin Guide

Here are the key plugins installed and how to use them:

## Navigation

*Easymotion* - Quick movement between lines
- Press `\\` followed by `w` or any motion key
- Words will be highlighted; jump to them by pressing the highlighted letter
- `\\j` to jump to any line below cursor
- `\\k` to jump to any line above cursor
- `\\f{char}` to jump to specific character on current line

*NERDTree* - File explorer
- Type `:NERDTree` or press `\d` to open the directory tree
- Navigate with normal vim movements
- Press `o` to open files or expand directories
- Press `t` to open file in new tab
- Press `i` to open file in horizontal split
- Press `s` to open file in vertical split
- Press `I` to toggle hidden files
- Press `m` to show the NERDTree menu (create/delete/move files)
- Press `?` to toggle help

*fzf.vim* - Fuzzy finder for files and content
- Press `\f` to search for files in current directory
- Press `\g` to search for text content within files
- Type `:Buffers` to list and switch between open buffers
- Type `:History:` to search command history
- Type `:History/` to search search history
- Type `:Commits` to browse git commits
- In the fzf window:
  - `Ctrl+t` to open in a new tab
  - `Ctrl+x` to open in a horizontal split
  - `Ctrl+v` to open in a vertical split

*MRU* - Most Recently Used files
- Press `\m` to show a list of recently opened files
- Navigate with j/k and press Enter to open

*vim-tmux-navigator* - Seamless navigation between vim and tmux
- Use `Ctrl+h/j/k/l` to navigate between vim splits and tmux panes
- Works across vim panes and tmux panes without having to use tmux prefix

## Editing

*vim-surround* - Work with surrounding pairs (quotes, brackets, tags)
- `cs"'` - Change surrounding quotes from double to single
- `cs']` - Change surrounding single quotes to square brackets
- `cs[<q>` - Change square brackets to HTML tags
- `ds"` - Delete surrounding quotes
- `ysiw]` - Add surrounding brackets to a word
- `yss)` - Wrap entire line in parentheses
- `ys2w"` - Surround 2 words with quotes
- `viw S<p>` - In visual mode, surround selection with HTML paragraph tags

*delimitMate* - Auto-close pairs of quotes, brackets, etc. as you type
- Automatically inserts closing brackets, quotes, etc. when you type the opening one
- Skips over closing character if already exists
- Expands carriage returns between brackets (type Enter between brackets)
- Supports custom mappings for specific file types

*vim-gitgutter* - Shows git diff markers in the gutter
- See which lines are added, modified, or removed in real-time
- `]c` - Jump to next change
- `[c` - Jump to previous change
- `<leader>hp` - Preview hunk changes under cursor
- `<leader>hs` - Stage the hunk under cursor
- `<leader>hu` - Undo the hunk under cursor

*Gundo* - Visualize your undo history
- Press `\u` to toggle the undo tree
- Navigate through your edit history with diffs
- Use j/k to move up and down through undo states
- Press Enter to revert to selected state
- Press 'p' to preview diff for a change

## Other Tools

*Python Docs*
- With cursor over a Python function, press `K` to open documentation in a split
- Works for built-in functions, modules and many popular libraries
- Use `Ctrl+W` followed by `o` to close the documentation split

*vim-startify* - Better start screen
- Shows MRU files, bookmarks, and sessions when vim starts
- Press `i` to create or save a session
- Navigate with j/k and press Enter to open
- Easily switch between projects with session management
- Add bookmarks by editing your vimrc to include:
  ```vim
  let g:startify_bookmarks = [ {'c': '~/.vimrc'}, {'z': '~/.zshrc'} ]
  ```

*vim-airline* - Enhanced status bar
- Shows file information, git branch, and more
- Displays current mode, encoding, file format
- Integrates with various plugins (gitgutter, syntastic, etc.)
- Shows error/warning count from linters
- Customizable themes (check `:help airline-themes`)

*Syntastic* - Syntax checking
- Automatically checks files for syntax errors when saving
- `:SyntasticCheck` - manually run syntax check
- `:SyntasticToggleMode` - toggle active/passive mode
- `:SyntasticInfo` - show checker information for current file
- Jump between errors with `:lnext` and `:lprev`

*vim-fugitive* - Git integration
- `:Gstatus` - show git status
- `:Gcommit` - commit changes
- `:Gblame` - show line-by-line git blame
- `:Gdiff` - show diff
- `:Glog` - load all previous revisions into the quickfix list

## Window Management
- Use `w+[hjkl]` to move between splits
- Use normal vim commands to create splits (`:split`, `:vsplit`)
- `Ctrl+w` + `v` - Create vertical split
- `Ctrl+w` + `s` - Create horizontal split
- `Ctrl+w` + `q` - Close current window
- `Ctrl+w` + `o` - Close all windows except current one
- `Ctrl+w` + `r` - Rotate windows
- `Ctrl+w` + `=` - Make all windows equal size

## Vim Tips
- `gg=G` - Automatically indent entire file
- `zt` - Move current line to top of screen
- `zz` - Move current line to middle of screen
- `zb` - Move current line to bottom of screen
- `zo` - Open fold under cursor
- `zc` - Close fold under cursor
- `zR` - Open all folds
- `zM` - Close all folds
- `gf` - Go to file under cursor
- `:s/old/new/g` - Search and replace in current line
- `:%s/old/new/g` - Search and replace in entire file
- `:%s/old/new/gc` - Search and replace in entire file with confirmation
- `:set list` - Show invisible characters (tabs, trailing spaces, etc.)
- `:set nolist` - Hide invisible characters

