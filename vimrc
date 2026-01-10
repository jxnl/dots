" ============================================================================
" VIM CONFIGURATION
" ============================================================================

" Colorscheme
colorscheme molokai
syntax enable
set t_Co=256
set encoding=utf8

" ============================================================================
" GENERAL SETTINGS
" ============================================================================

" Auto-reload files when changed externally
set autoread

" Better command-line completion
set wildmenu
set wildmode=full
set wildignore+=*.o,*.obj,.git,*.pyc,__pycache__

" Backspace behavior
set backspace=indent,eol,start

" Hidden buffers (switch without saving)
set hidden

" No error bells
set noerrorbells
set visualbell
set t_vb=

" ============================================================================
" INTERFACE
" ============================================================================

" Line numbers
set number
set ruler
set showcmd

" Search settings
set ignorecase
set smartcase
set hlsearch
set incsearch
set magic

" Show matching brackets
set showmatch
set mat=2

" Performance
set lazyredraw

" Cursor context
set scrolloff=10

" Display whitespace characters
set listchars=tab:>.,trail:.,precedes:<,extends:>
set list
set nowrap

" Modern mouse support
set mouse=a

" Clipboard integration (use system clipboard)
if has('clipboard')
  set clipboard=unnamed,unnamedplus
endif

" GUI options (remove scrollbars)
set guioptions-=r
set guioptions-=R
set guioptions-=l
set guioptions-=L

" Disable folding by default
set nofoldenable
set foldmethod=manual

" ============================================================================
" INDENTATION
" ============================================================================

" Default to 4 spaces
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set smarttab
set autoindent
set smartindent

" ============================================================================
" UNDO AND BACKUPS
" ============================================================================

" Disable backup files
set nobackup
set nowb
set noswapfile

" Persistent undo
set undofile
set undodir=~/.vim/undo
set undolevels=1000
set undoreload=10000

" Create undo directory if it doesn't exist
if !isdirectory($HOME . "/.vim/undo")
    call mkdir($HOME . "/.vim/undo", "p", 0700)
endif

" ============================================================================
" KEY MAPPINGS
" ============================================================================

" Set leader key
let mapleader = ","

" Fast save
nmap <leader>w :w<cr>

" Sudo save (for permission-denied errors)
command W w !sudo tee % > /dev/null

" Search mappings
map <space> /
map <c-space> ?

" Clear search highlight
nnoremap <leader><space> :nohlsearch<cr>

" Smart window navigation
map <leader>j <C-W>j
map <leader>k <C-W>k
map <leader>h <C-W>h
map <leader>l <C-W>l

" Tab navigation
nmap <S-Tab> <<

" Move lines up/down
nnoremap <A-j> :m .+1<CR>==
nnoremap <A-k> :m .-2<CR>==
vnoremap <A-j> :m '>+1<CR>gv=gv
vnoremap <A-k> :m '<-2<CR>gv=gv

" Better indentation in visual mode
vnoremap < <gv
vnoremap > >gv

" Optional: Disable arrow keys (uncomment to enable hardcore mode)
" noremap <Up> <NOP>
" noremap <Down> <NOP>
" noremap <Left> <NOP>
" noremap <Right> <NOP>

" ============================================================================
" AUTOCOMPLETE
" ============================================================================

set omnifunc=syntaxcomplete#Complete
set completeopt=menuone,longest,preview

" ============================================================================
" FILE TYPE SPECIFIC SETTINGS
" ============================================================================

" Python
autocmd FileType python setlocal colorcolumn=88
autocmd FileType python setlocal expandtab
autocmd FileType python setlocal textwidth=88
autocmd BufWrite *.py :call DeleteTrailingWS()

" JavaScript/TypeScript
autocmd FileType javascript,typescript,javascriptreact,typescriptreact setlocal sw=2 ts=2 sts=2
autocmd FileType json setlocal sw=2 ts=2 sts=2

" HTML/CSS
autocmd FileType html,css,scss setlocal sw=2 ts=2 sts=2

" YAML
autocmd FileType yaml setlocal sw=2 ts=2 sts=2

" Markdown
autocmd FileType markdown setlocal spell nonumber wrap linebreak

" Go
autocmd FileType go setlocal noexpandtab tabstop=4 shiftwidth=4

" ============================================================================
" UTILITY FUNCTIONS
" ============================================================================

" Delete trailing whitespace
func! DeleteTrailingWS()
  exe "normal mz"
  %s/\s\+$//ge
  exe "normal `z"
endfunc

" ============================================================================
" PLUGIN MANAGER (vim-plug)
" ============================================================================

set nocompatible
filetype off

" Auto-install vim-plug if not present
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

call plug#begin('~/.vim/plugged')

" ============================================================================
" ESSENTIAL PLUGINS
" ============================================================================

" Sensible defaults
Plug 'tpope/vim-sensible'

" Text manipulation
Plug 'tpope/vim-surround'          " Surround text objects
Plug 'tpope/vim-repeat'            " Repeat plugin commands
Plug 'tpope/vim-commentary'        " Smart commenting
Plug 'jiangmiao/auto-pairs'        " Auto close brackets
Plug 'wellle/targets.vim'          " Additional text objects
Plug 'easymotion/vim-easymotion'   " Fast navigation
Plug 'machakann/vim-highlightedyank'  " Highlight yanked text

" ============================================================================
" FILE NAVIGATION AND SEARCH
" ============================================================================

Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
Plug 'preservim/nerdtree'
Plug 'Xuyuanp/nerdtree-git-plugin'
Plug 'vim-scripts/mru.vim'

" ============================================================================
" GIT INTEGRATION
" ============================================================================

Plug 'tpope/vim-fugitive'          " Git commands
Plug 'airblade/vim-gitgutter'      " Git diff in gutter

" ============================================================================
" UI AND APPEARANCE
" ============================================================================

Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'mhinz/vim-startify'          " Start screen

" ============================================================================
" PYTHON DEVELOPMENT
" ============================================================================

Plug 'dense-analysis/ale'                    " Async linting
Plug 'psf/black', { 'branch': 'stable' }     " Black formatter
Plug 'vim-python/python-syntax'              " Enhanced Python syntax
Plug 'Vimjas/vim-python-pep8-indent'         " PEP8 indentation
Plug 'jeetsukumaran/vim-pythonsense'         " Python text objects

if has('python3')
  Plug 'davidhalter/jedi-vim'                " Python completion
endif

" ============================================================================
" WEB DEVELOPMENT
" ============================================================================

Plug 'mattn/emmet-vim'                       " HTML/CSS expansion
Plug 'pangloss/vim-javascript'               " JavaScript support
Plug 'leafgarland/typescript-vim'            " TypeScript syntax
Plug 'maxmellon/vim-jsx-pretty'              " JSX syntax

" ============================================================================
" MARKDOWN AND DOCUMENTATION
" ============================================================================

Plug 'preservim/vim-markdown'
Plug 'lervag/vimtex'                         " LaTeX support

" ============================================================================
" SNIPPETS
" ============================================================================

Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'

" ============================================================================
" UTILITIES
" ============================================================================

Plug 'sjl/gundo.vim'                         " Undo tree
Plug 'christoomey/vim-tmux-navigator'        " Tmux integration

call plug#end()

" ============================================================================
" PLUGIN CONFIGURATIONS
" ============================================================================

" Airline
let g:airline#extensions#tabline#enabled = 1
let g:airline_theme='dark'
let g:airline_powerline_fonts = 1
set laststatus=2
set ttimeoutlen=50

" ALE - Async Lint Engine (modern linting)
let g:ale_linters = {
\   'python': ['ruff', 'mypy'],
\   'javascript': ['eslint'],
\   'typescript': ['eslint', 'tsserver'],
\}
let g:ale_fixers = {
\   'python': ['black', 'ruff'],
\   'javascript': ['prettier', 'eslint'],
\   'typescript': ['prettier', 'eslint'],
\   'json': ['prettier'],
\   'yaml': ['prettier'],
\   'markdown': ['prettier'],
\}
let g:ale_fix_on_save = 1
let g:ale_python_ruff_options = '--line-length=88'
let g:ale_python_black_options = '--line-length=88'

" Enhanced Python syntax
let g:python_highlight_all = 1

" Jedi-vim
let g:jedi#auto_initialization = 1
let g:jedi#completions_enabled = 1
let g:jedi#show_call_signatures = 1
let g:jedi#smart_auto_mappings = 0

" FZF
nnoremap <leader>f :Files<CR>
nnoremap <leader>g :Rg<CR>
nnoremap <leader>b :Buffers<CR>
nnoremap <leader>/ :History<CR>

" NERDTree
nnoremap <leader>d :NERDTreeToggle<CR>
nnoremap <leader>n :NERDTreeFind<CR>
let NERDTreeShowHidden=1
let NERDTreeIgnore=['\.pyc$', '\.pyo$', '__pycache__', '\.git$', 'node_modules']

" Auto-close NERDTree if it's the last window
autocmd BufEnter * if winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif

" MRU (Most Recently Used)
nnoremap <leader>m :MRU<CR>

" Gundo (undo tree)
nnoremap <leader>u :GundoToggle<CR>

" Black formatting
nnoremap <leader>bl :Black<CR>

" UltiSnips
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<c-b>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"

" Vim-markdown (disable all folding)
let g:vim_markdown_folding_disabled = 1
let g:vim_markdown_folding_level = 99
let g:vim_markdown_new_list_item_indent = 0
let g:vim_markdown_frontmatter = 1
let g:vim_markdown_auto_insert_bullets = 0
let g:vim_markdown_conceal = 0

" Emmet
let g:user_emmet_leader_key='<C-e>'

" ============================================================================
" FINAL SETTINGS
" ============================================================================

filetype plugin indent on

" Auto-source vimrc on save
autocmd! BufWritePost $MYVIMRC source $MYVIMRC
