" Wrapping and tabs.
set tabstop=4
set softtabstop=4
set shiftwidth=4
set textwidth=80
set smarttab
set expandtab

set lbr
set tw=500

set ai "Auto indent
set si "Smart indet
set wrap "Wrap lines

colorscheme molokai

command! W :w

" Allow pasting blocks of code without indenting
set pastetoggle=<F2>

"Fix Shift+Tab
nmap <S-Tab> <<
imap <S-Tab> <Esc><<i

" Basic Settings
syntax on                     " syntax highlighing
filetype on                   " try to detect filetypes
filetype plugin indent on     " enable loading indent file for filetype
set number                    " Display line numbers
set numberwidth=1             " using only 1 column (and 1 space) while possible
set title                     " show title in console title bar
set wildmenu                  " Menu completion in command mode on <Tab>
set wildmode=full             " <Tab> cycles between all matching choices.
set showcmd

set colorcolumn=80
inoremap # #
set ls=2  "Always show status line"
set ruler
set hidden
set nolazyredraw
set showmatch
set encoding=utf8

set backspace=indent,eol,start

" Set autocomplete form 
set completeopt=menuone,longest,preview

"--- python formatting help ---
autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class

" Enable omni completion.
autocmd FileType css set omnifunc=csscomplete#CompleteCSS
autocmd FileType html,markdown,ctp set omnifunc=htmlcomplete#CompleteTags
autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
autocmd FileType python set omnifunc=pythoncomplete#Complete
autocmd FileType xml set omnifunc=xmlcomplete#CompleteTags
autocmd FileType php,ctp set omnifunc=phpcomplete#CompletePHP
autocmd FileType vim set omnifunc=syntaxcomplete#Complete

" markdown
au BufEnter,Bufread *.mkd,*.md,*.mdown,*.markdown set tw=0

" HTML (tab width 2 chr, no wrapping)
autocmd FileType html set sw=2
autocmd FileType html set ts=2
autocmd FileType html set sts=2
autocmd FileType html set textwidth=0

" CSS (tab width 2 chr, wrap at 79th char)
autocmd FileType css set sw=2
autocmd FileType css set ts=2
autocmd FileType css set sts=2

"remove trailing whitespace
autocmd BufWritePre *.c :%s/\s\+$//e
autocmd BufWritePre *.cpp :%s/\s\+$//e
autocmd BufWritePre *.c++ :%s/\s\+$//e
autocmd BufWritePre *.h :%s/\s\+$//e
autocmd BufWritePre *.java :%s/\s\+$//e
autocmd BufWritePre *.php :%s/\s\+$//e
autocmd BufWritePre *.pl :%s/\s\+$//e
autocmd BufWritePre *.py :%s/\s\+$//e

set nobackup
set nowb
set noswapfile

set undodir=~/.vim/undodir
set undofile
set undolevels=1000 "maximum number of changes that can be undone
set undoreload=10000 "maximum number lines to save for undo on a buffer reload
language en_US
 
set undodir=~/.vim_runtime/undodir
set undofile

" Moving tab using CTRL+ the arrows
map <C-right> :bn<CR>
map <C-left> :bp<CR>

" displays tabs with :set list & displays when a line runs off-screen
set listchars=tab:>.,trail:.,precedes:<,extends:>
set list
 
""" Searching and Patterns
set ignorecase              " Default to using case insensitive searches,
set smartcase               " unless uppercase letters are used in the regex.
set smarttab                " Handle tabs more intelligently
set hlsearch                " Highlight searches by default.
set incsearch               " Incrementally search while typing a /regex
 
" Ignore these files when completing
set wildignore+=*.o,*.obj,.git,*.pyc
set wildignore+=eggs/**
set wildignore+=*.egg-info/**

set nocompatible              " be iMproved, required
filetype off                  " required

 set rtp+=~/.vim/bundle/vundle/
 call vundle#rc()

" let Vundle manage Vundle, required
Bundle 'gmarik/vundle'

" Utilities
Bundle "tsaleh/vim-matchit"
Bundle 'Raimondi/delimitMate'

Bundle 'mattn/emmet-vim'
Bundle 'tpope/vim-fugitive'
Bundle 'Lokaltog/vim-easymotion'

" Syntax Commenter
Bundle 'vim-scripts/tComment'

" Python Syntax Checker
Bundle 'kevinw/pyflakes-vim'
Bundle 'vim-scripts/pep8'
Bundle 'vim-scripts/Pydiction'
Bundle "vim-scripts/indentpython.vim"

" HTML Development 
Bundle 'rstacruz/sparkup', {'rtp': 'vim/'}

" Universal Syntax Checker + Completion
"Bundle 'UltiSnips'
Bundle 'scrooloose/syntastic'
"Bundle "Shougo/neocomplcache"

" Files manager
Bundle 'majutsushi/tagbar'
Bundle 'L9'
Bundle 'FuzzyFinder'
Bundle 'vim-scripts/mru.vim'
Bundle 'fholgado/minibufexpl.vim'
Bundle 'scrooloose/nerdtree'
Bundle 'jistr/vim-nerdtree-tabs'
Bundle 'sjl/gundo.vim'

filetype plugin indent on

" Pep8 using F6
" You can change with this :
let g:pep8_map='<F6>'

" Pydiction
let g:pydiction_location='/home/ubuntu/.vim/bundle/Pydiction/complete-dict'

"""" PYTHON STYLE """"
let python_highlight_all=1 " Enable all plugin's highlighting.
let python_slow_sync=1 " For fast machines.
let python_print_as_function=1 " Color 'print' function.

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" FuzzFinder Shorcuts. Using F2 for opening FuzzyFinderTextMate
map <leader>f :FufFileWithCurrentBufferDir<CR>
map <leader>m :FufFileWithFullCwd<CR>
map <leader>b :FufBuffer<CR>

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" MRU shorcuts
map <leader><space> :MRU<CR> 

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Pyflakes configuration
if has("gui_running")
    highlight SpellBad term=underline gui=undercurl guisp=Orange
endif

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Configure neocomplcache autocomplete 
" http://www.vim.org/scripts/script.php?script_id=2620

highlight Pmenu gui=bold

if has("gui_running")
    highlight SpellBad term=underline gui=undercurl guisp=Orange
endif

