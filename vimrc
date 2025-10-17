colorscheme molokai

syntax enable

" Set to read when a file is changed
set autoread

set t_Co=256
set backspace=indent,eol,start
set omnifunc=syntaxcomplete#Complete

"==============="
" HARDCORE MODE "
"==============="

" FUCK YO SCROLLBARS
set guioptions-=r
set guioptions-=R
set guioptions-=l
set guioptions-=L

" FUCK YO ARROW KEYS
noremap <Up> <NOP>
noremap <Down> <NOP>
noremap <Left> <NOP>
noremap <Right> <NOP>

"============="
" INDENTATION "
"============="

" Render tabs as 4 spaces
set tabstop=4                   " Tabs are four spaces
set softtabstop=4               " Tabs counts as four spaces
set shiftwidth=4                " << >> gives you four spaces

" For those who have the sanity to use 4 spaces
set smarttab
set expandtab

set autoindent                  " Auto indent
set smartindent                 " Smart indent

" Displays tabs with :set list
" Displays when a line runs off-screen
set listchars=tab:>.,trail:.,precedes:<,extends:>
set list
set nowrap                      " Dont wrap lines
set so=10                        " set 10 lines to the cursor

"================"
" REMAPPING KEYS "
"================"

" fast save
nmap ww :w<cr>

" :W sudo saves the file 
" (useful for handling the permission-denied error)
command W w !sudo tee % > /dev/null

" Map <Space> to / (search) and Ctrl-<Space> to ? (backwards search)
map <space> /
map <C-space> ?

" Smart way to move between windows
map  wj <C-W>j
map  wk <C-W>k
map  wh <C-W>h
map  wl <C-W>l

" << >> gives me tabs
nmap <S-Tab> <<

"==========="
" INTERFACE "
"==========="

set ruler                       " Show current position
set showmatch                   " Show matching parens
set number                      " Display line numbers
set wildmenu                    " Menu completion in command mode on <Tab>
set wildmode=full               " <Tab> cycles between all matching choices.
set showcmd                     " Show last command
set encoding=utf8
set hid
set ignorecase
set smartcase
set hlsearch
set incsearch 
set lazyredraw 
set magic
set showmatch 
set mat=2

"=================="
" UNDO AND BACKUPS "
"=================="

" Fuck backup files
set nobackup
set nowb
set noswapfile

" Undo
set undofile                " Save undo's after file closes
set undodir=~/.vim/undo     " where to save undo histories
set undolevels=1000         " How many undos
set undoreload=10000        " number of lines to save for undo

" Use Unix as the standard file type
set ffs=unix,dos,mac

" Set autocomplete form
set completeopt=menuone,longest,preview

" Python reindents 
autocmd BufRead python set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class,
autocmd BufRead python set colorcolumn=80

" Markdown
autocmd FileType markdown set spell
autocmd FileType markdown set nonumber

" CSS (tab width 2 chr, wrap at 79th char)
autocmd FileType css set sw=2
autocmd FileType css set ts=2
autocmd FileType css set sts=2

" Delete trailing white space on save, useful for Python and CoffeeScript ;)
func! DeleteTrailingWS()
  exe "normal mz"
  %s/\s\+$//ge
  exe "normal `z"
endfunc

autocmd BufWrite *.py :call DeleteTrailingWS()

" Ignore these files when completing
set wildignore+=*.o,*.obj,.git,*.pyc

"===================="
" STOP, Vundle time~ "
"===================="

set nocompatible              " be iMproved, required
filetype off                  " required

set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

" let Vundle manage Vundle, required
Bundle "gmarik/vundle"

" Utilities
Bundle "Raimondi/delimitMate"
Bundle "honza/vim-snippets"
Bundle "tpope/vim-fugitive"
Bundle "Lokaltog/vim-easymotion"
Bundle "scrooloose/nerdcommenter"
Bundle "bling/vim-airline"
    let g:airline#extensions#tabline#enabled = 1
    set laststatus=2
    set ttimeoutlen=50

" Html
Bundle "mattn/emmet-vim"

" Universal Syntax Checker + Completion
Bundle "scrooloose/syntastic"

" Files manager
Bundle "junegunn/fzf"
Bundle "junegunn/fzf.vim"
    " \f to find files in current directory
    map <leader>f :Files<CR>
    " \g to search content in files
    map <leader>g :Rg<CR>
Bundle "vim-scripts/mru.vim"
    " \m to show most recently used files
    map <leader>m :MRU<CR>

" Directories and tables
Bundle "jistr/vim-nerdtree-tabs"
Bundle "scrooloose/nerdtree"
    nnoremap <Leader>d :NERDTree<CR>
    " \d shows you the directory tree

" Magical Gundo
Bundle "sjl/gundo.vim"
    nnoremap <Leader>u :GundoToggle<CR>
    " \u shows you the undo history

" LaTeX
Bundle "jcf/vim-latex"

" Markdown
Bundle "plasticboy/vim-markdown"

Bundle 'hdima/python-syntax'

let g:syntastic_python_checkers = ['ruff']

" Additional modern plugins
Bundle "tpope/vim-surround"
Bundle "airblade/vim-gitgutter"
Bundle "christoomey/vim-tmux-navigator"
Bundle "mhinz/vim-startify"

filetype plugin on
filetype indent on
