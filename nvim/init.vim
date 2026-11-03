" Source shared configurations
set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
source ~/.vimrc

" Neovim specific settings
set termguicolors
if executable('python3')
  let g:python3_host_prog = exepath('python3')
endif

lua << EOF
-- Allow first startup before :PlugInstall has populated the plugin directory.
local function setup(name, options)
  local ok, plugin = pcall(require, name)
  if ok then plugin.setup(options or {}) end
end
setup('telescope', { defaults = {
  file_ignore_patterns = { 'node_modules/', '%.git/' },
  layout_strategy = 'flex',
} })
setup('which-key')
setup('gitsigns')
setup('trouble')
setup('ibl', { scope = { enabled = true } })

if vim.fn.has('nvim-0.11') == 1 and #vim.api.nvim_get_runtime_file('lsp/pyright.lua', false) > 0 then
  vim.lsp.enable({ 'pyright', 'gopls', 'rust_analyzer' })
end
vim.api.nvim_create_autocmd('FileType', {
  group = vim.api.nvim_create_augroup('dots_treesitter', { clear = true }),
  pattern = { 'python', 'lua', 'vim', 'go', 'rust', 'markdown' },
  callback = function(event)
    local lang = vim.treesitter.language.get_lang(event.match)
    if lang and vim.treesitter.language.add(lang) then vim.treesitter.start(event.buf, lang) end
  end,
})
EOF

" Neovim specific keymaps
nnoremap <silent> gd    <cmd>lua vim.lsp.buf.definition()<CR>
nnoremap <silent> gh    <cmd>lua vim.lsp.buf.hover()<CR>
nnoremap <silent> gD    <cmd>lua vim.lsp.buf.implementation()<CR>
nnoremap <silent> <c-k> <cmd>lua vim.lsp.buf.signature_help()<CR>
nnoremap <silent> gr    <cmd>lua vim.lsp.buf.references()<CR>
nnoremap <silent> g0    <cmd>lua vim.lsp.buf.document_symbol()<CR>
nnoremap <silent> gW    <cmd>lua vim.lsp.buf.workspace_symbol()<CR>
nnoremap <silent> ga    <cmd>lua vim.lsp.buf.code_action()<CR>
