" ============================================================================
" VIM CONFIGURATION
" ============================================================================

" Keep Vim in script mode
set nocompatible

" Colors and syntax
if has('termguicolors')
  set termguicolors
endif
colorscheme molokai
syntax enable
set encoding=utf-8

" ============================================================================
" GENERAL SETTINGS
" ============================================================================

" Auto-reload files when changed externally
set autoread

" Better command-line completion
set wildmenu
set wildmode=full
set wildignore+=*.o,*.obj,.git,*.pyc,__pycache__
set shortmess+=I

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
set relativenumber
set ruler
set showcmd
set signcolumn=yes

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
set updatetime=250
set synmaxcol=240
set redrawtime=1500

" Cursor context
set scrolloff=10
set splitbelow
set splitright

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
if has('gui_running')
  set guioptions-=r
  set guioptions-=R
  set guioptions-=l
  set guioptions-=L
endif

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
set nowritebackup
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
nnoremap <leader>w :w<cr>

" Sudo save (for permission-denied errors). The bang makes reloads idempotent.
command! W write !sudo tee % > /dev/null

" Search mappings
nnoremap <space> /
nnoremap <c-space> ?

" Clear search highlight
nnoremap <leader><space> :nohlsearch<cr>

" Smart window navigation
nnoremap <leader>j <C-W>j
nnoremap <leader>k <C-W>k
nnoremap <leader>h <C-W>h
nnoremap <leader>l <C-W>l

" Tab navigation
nnoremap <S-Tab> <<

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

" FileType + write autocmds (deduplicated on reload)
augroup user_filetype_settings
  autocmd!
  " Python
  autocmd FileType python setlocal colorcolumn=88 textwidth=88 expandtab
  autocmd BufWritePre *.py call DeleteTrailingWS()

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
augroup END

" ============================================================================
" UTILITY FUNCTIONS
" ============================================================================

" Delete trailing whitespace
function! DeleteTrailingWS()
  let l:save_view = winsaveview()
  silent! keeppatterns %s/\s\+$//ge
  call winrestview(l:save_view)
endfunc

" ============================================================================
" PLUGIN MANAGER (vim-plug)
" ============================================================================

filetype off

" Auto-install vim-plug if not present
augroup user_plug_bootstrap
  autocmd!
  if empty(glob('~/.vim/autoload/plug.vim'))
    silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
      \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
    autocmd VimEnter * nested PlugInstall --sync | source $MYVIMRC
  endif
augroup END

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
Plug 'preservim/nerdtree', { 'on': ['NERDTreeToggle', 'NERDTreeFind'] }
Plug 'Xuyuanp/nerdtree-git-plugin', { 'on': ['NERDTreeToggle', 'NERDTreeFind'] }
Plug 'vim-scripts/mru.vim', { 'on': ['MRU'] }

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
Plug 'psf/black', { 'branch': 'stable', 'for': 'python' }     " Black formatter
Plug 'vim-python/python-syntax', { 'for': 'python' }              " Enhanced Python syntax
Plug 'Vimjas/vim-python-pep8-indent', { 'for': 'python' }         " PEP8 indentation
Plug 'jeetsukumaran/vim-pythonsense', { 'for': 'python' }         " Python text objects

if has('python3')
  Plug 'davidhalter/jedi-vim', { 'for': 'python' }                " Python completion
endif

" ============================================================================
" WEB DEVELOPMENT
" ============================================================================

Plug 'mattn/emmet-vim', { 'for': ['html', 'css', 'scss', 'jsx', 'tsx'] }                       " HTML/CSS expansion
Plug 'pangloss/vim-javascript', { 'for': ['javascript', 'javascriptreact'] }               " JavaScript support
Plug 'leafgarland/typescript-vim', { 'for': ['typescript', 'typescriptreact'] }            " TypeScript syntax
Plug 'maxmellon/vim-jsx-pretty', { 'for': ['javascriptreact', 'typescriptreact', 'jsx', 'tsx'] }              " JSX syntax

" ============================================================================
" MARKDOWN AND DOCUMENTATION
" ============================================================================

Plug 'preservim/vim-markdown', { 'for': 'markdown' }
Plug 'lervag/vimtex', { 'for': 'tex' }                         " LaTeX support

" ============================================================================
" SNIPPETS
" ============================================================================

Plug 'SirVer/ultisnips', { 'for': ['python', 'javascript', 'typescript', 'markdown', 'yaml', 'json', 'html', 'css'] }
Plug 'honza/vim-snippets', { 'for': ['python', 'javascript', 'typescript', 'markdown', 'yaml', 'json', 'html', 'css'] }

" ============================================================================
" UTILITIES
" ============================================================================

Plug 'sjl/gundo.vim', { 'on': 'GundoToggle' }                         " Undo tree
Plug 'christoomey/vim-tmux-navigator'        " Tmux integration

" ============================================================================
" NEOVIM-ONLY PLUGINS
" ============================================================================

if has('nvim')
  Plug 'nvim-lua/plenary.nvim'               " Lua helpers (required by Telescope)
  Plug 'nvim-treesitter/nvim-treesitter', { 'do': ':TSUpdate' }
  Plug 'neovim/nvim-lspconfig'
  Plug 'nvim-telescope/telescope.nvim'
  Plug 'folke/which-key.nvim'
  Plug 'lewis6991/gitsigns.nvim'
  Plug 'folke/trouble.nvim'
  Plug 'lukas-reineke/indent-blankline.nvim'
endif

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
augroup user_nerdtree
  autocmd!
  autocmd BufEnter * if winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif
augroup END

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
augroup user_vimrc_reload
  autocmd!
  autocmd BufWritePost $MYVIMRC source $MYVIMRC
augroup END

" Open Codex in a terminal split without leaving the current buffer.
if executable('codex') && exists(':terminal') == 2
  if has('nvim')
    command! Codex split | execute 'terminal codex' | startinsert
    command! CodexResume split | execute 'terminal codex resume --last' | startinsert
  else
    command! Codex terminal codex
    command! CodexResume terminal codex resume --last
  endif
endif
