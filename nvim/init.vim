" Source shared configurations
set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
source ~/.vimrc

" Neovim specific settings
set termguicolors
if executable('python3')
  let g:python3_host_prog = system('command -v python3')
  let g:python3_host_prog = substitute(g:python3_host_prog, '\n', '', 'g')
endif

" Use native LSP instead of CoC for Neovim
lua << EOF
require('nvim-treesitter.configs').setup {
    ensure_installed = { "python", "lua", "vim", "go", "rust", "markdown" },
    highlight = {
        enable = true,
    },
}

-- Native LSP Setup
local lspconfig = require('lspconfig')
lspconfig.pyright.setup{}
lspconfig.gopls.setup{}
lspconfig.rust_analyzer.setup{}

-- Telescope setup
require('telescope').setup{
    defaults = {
        file_ignore_patterns = {"node_modules", ".git"},
        layout_strategy = 'flex',
    }
}

-- Which Key setup
require('which-key').setup{}

-- Git signs setup
require('gitsigns').setup()

-- Trouble setup
require('trouble').setup{
    position = "bottom",
    height = 10,
    icons = true,
    mode = "workspace_diagnostics",
    fold_open = "",
    fold_closed = "",
    group = true,
    padding = true,
    action_keys = {
        close = "q",
        cancel = "<esc>",
        refresh = "r",
        jump = {"<cr>", "<tab>"},
        open_split = { "<c-x>" },
        open_vsplit = { "<c-v>" },
        open_tab = { "<c-t>" },
        jump_close = {"o"},
        toggle_mode = "m",
        toggle_preview = "P",
        hover = "K",
        preview = "p",
        close_folds = {"zM", "zm"},
        open_folds = {"zR", "zr"},
        toggle_fold = {"zA", "za"},
        previous = "k",
        next = "j"
    },
}

-- Indent blankline setup
require('indent_blankline').setup {
    show_current_context = true,
    show_current_context_start = true,
}
EOF

" Neovim specific keymaps
nnoremap <silent> gd    <cmd>lua vim.lsp.buf.definition()<CR>
nnoremap <silent> gh    <cmd>lua vim.lsp.buf.hover()<CR>
nnoremap <silent> gD    <cmd>lua vim.lsp.buf.implementation()<CR>
nnoremap <silent> <c-k> <cmd>lua vim.lsp.buf.signature_help()<CR>
nnoremap <silent> gr    <cmd>lua vim.lsp.buf.references()<CR>
nnoremap <silent> g0    <cmd>lua vim.lsp.buf.document_symbol()<CR>
nnoremap <silent> gW    <cmd>lua vim.lsp.buf.workspace_symbol()<CR>
nnoremap <silent> gd    <cmd>lua vim.lsp.buf.definition()<CR>
nnoremap <silent> ga    <cmd>lua vim.lsp.buf.code_action()<CR> 
