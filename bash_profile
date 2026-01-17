alias bashrc='source ~/.bash_profile'

# Prefer Neovim when available; fall back to Vim.
if command -v nvim >/dev/null 2>&1; then
  export EDITOR="nvim"
  export VISUAL="nvim"
  export GIT_EDITOR="nvim"
  alias vim='nvim'
  alias v='nvim'
else
  export EDITOR="vim"
  export VISUAL="vim"
  export GIT_EDITOR="vim"
  alias v='vim'
fi

# Shell safety defaults
set -o noclobber
alias clobber='set +o noclobber'

# Change Prompt
export PS1="\w : \h (\u) \n>>> " 
export PS2="  > "

# Colors
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced

# Terminal Preferences
if command -v trash >/dev/null 2>&1; then
  alias rm='trash'
  alias remove='trash -i'
else
alias rm='echo "rm is disabled, install trash or use /bin/rm instead."'
  alias remove='echo "remove is disabled, install trash or use /bin/rm instead."'
fi
alias cp='cp -iv'                           # Preferred 'cp' implementation
alias mv='mv -iv'                           # Preferred 'mv' implementation
alias ln='ln -iv'                           # Safer symlink creation
alias mkdir='mkdir -pv'                     # Preferred 'mkdir' implementation
alias cd..='cd ../'                         # Go back 1 directory level (for fast typers)
alias ..='cd ../'                           # Go back 1 directory level
alias ...='cd ../../'                       # Go back 2 directory levels
alias ~="cd ~"                              # ~:            Go Home
alias c='clear'                             # c:            Clear terminal display

#   lr:  Full Recursive Directory Listing
#   ------------------------------------------
alias lr='ls -R | grep ":$" | sed -e '\'s/:$//'\'' -e '\''s/[^-][^\/]*\//--/g'\'' -e '\''s/^/   /'\'' -e '\''s/-/|/'\'' | less'
