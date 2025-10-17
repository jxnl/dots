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

" Disable folding
set nofoldenable
set foldmethod=manual

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
autocmd FileType markdown set nofoldenable

" HTML (tab width 2 chr, no wrapping)
autocmd FileType html set sw=2
autocmd FileType html set ts=2
autocmd FileType html set sts=2

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

" Modern plugin manager - vim-plug (faster than Vundle)
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

call plug#begin('~/.vim/plugged')

" Core utilities
Plug 'tpope/vim-sensible'          " Sensible defaults
Plug 'tpope/vim-surround'          " Surround text objects
Plug 'tpope/vim-repeat'            " Repeat plugin commands with .
Plug 'tpope/vim-fugitive'          " Git integration
Plug 'tpope/vim-commentary'        " Smart commenting
Plug 'jiangmiao/auto-pairs'        " Auto close brackets

" Modern file navigation and search
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
Plug 'preservim/nerdtree'
Plug 'Xuyuanp/nerdtree-git-plugin'
Plug 'vim-scripts/mru.vim'

" Status line and UI
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'airblade/vim-gitgutter'
Plug 'mhinz/vim-startify'

" Python development stack
Plug 'dense-analysis/ale'          " Modern async linting (replaces syntastic)
Plug 'psf/black', { 'branch': 'stable' }
" Plug 'fisadev/vim-isort'          " Import sorting (disabled - no Python support)
Plug 'vim-python/python-syntax'   " Better Python syntax
Plug 'Vimjas/vim-python-pep8-indent'  " PEP8 indentation
Plug 'jeetsukumaran/vim-pythonsense'  " Python text objects

" Completion and snippets
if has('python3')
  Plug 'davidhalter/jedi-vim'     " Python completion
endif
Plug 'SirVer/ultisnips'           " Snippets engine
Plug 'honza/vim-snippets'         " Snippet collection

" Enhanced editing
Plug 'easymotion/vim-easymotion'  " Fast navigation
Plug 'wellle/targets.vim'        " Additional text objects
Plug 'machakann/vim-highlightedyank'  " Highlight yanked text

" Web development (keeping your existing)
Plug 'mattn/emmet-vim'

" LaTeX and Markdown
Plug 'lervag/vimtex'             " Modern LaTeX plugin
Plug 'preservim/vim-markdown'

" Terminal integration
Plug 'christoomey/vim-tmux-navigator'

" Undo visualization
Plug 'sjl/gundo.vim'

call plug#end()

" Plugin configurations
" Airline
let g:airline#extensions#tabline#enabled = 1
let g:airline_theme='dark'
let g:airline_powerline_fonts = 1
set laststatus=2
set ttimeoutlen=50

" ALE (Async Lint Engine) - modern replacement for syntastic
let g:ale_linters = {
\   'python': ['ruff', 'mypy'],
\}
let g:ale_fixers = {
\   'python': ['black', 'ruff'],
\}
let g:ale_fix_on_save = 1
let g:ale_python_ruff_options = '--line-length=88'
let g:ale_python_black_options = '--line-length=88'

" Enhanced Python syntax
let g:python_highlight_all = 1

" Jedi-vim configuration
let g:jedi#auto_initialization = 1
let g:jedi#completions_enabled = 1
let g:jedi#show_call_signatures = 1

" FZF mappings
nnoremap <leader>f :Files<CR>
nnoremap <leader>g :Rg<CR>
nnoremap <leader>b :Buffers<CR>
nnoremap <leader>h :History<CR>

" NERDTree
nnoremap <Leader>d :NERDTreeToggle<CR>
let NERDTreeShowHidden=1
let NERDTreeIgnore=['\.pyc$', '\.pyo$', '__pycache__']

" MRU
nnoremap <leader>m :MRU<CR>

" Gundo
nnoremap <Leader>u :GundoToggle<CR>

" Black formatting
nnoremap <leader>bl :Black<CR>

" UltiSnips
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<c-b>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"

" Disable vim-markdown folding
let g:vim_markdown_folding_disabled = 1

filetype plugin on
filetype indent on
