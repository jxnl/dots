alias bashrc='source ~/.bash_profile'

# Change Prompt
export PS1="\w : \h (\u) \n>>> " 
export PS2="  > "

# Colors
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced

# Terminal Preferences
alias rm='echo "rm is disabled, use trash or /bin/rm instead."'
alias remove='rm -irv'
alias cp='cp -iv'                           # Preferred 'cp' implementation
alias mv='mv -iv'                           # Preferred 'mv' implementation
alias mkdir='mkdir -pv'                     # Preferred 'mkdir' implementation
alias cd..='cd ../'                         # Go back 1 directory level (for fast typers)
alias ..='cd ../'                           # Go back 1 directory level
alias ...='cd ../../'                       # Go back 2 directory levels
alias ~="cd ~"                              # ~:            Go Home
alias c='clear'                             # c:            Clear terminal display

#   lr:  Full Recursive Directory Listing
#   ------------------------------------------
alias lr='ls -R | grep ":$" | sed -e '\'s/:$//'\'' -e '\''s/[^-][^\/]*\//--/g'\'' -e '\''s/^/   /'\'' -e '\''s/-/|/'\'' | less'
