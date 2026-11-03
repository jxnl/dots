# dots

My terminal setup for editing in Vim, running Codex alongside it, and keeping a project open in tmux.

## Everyday commands

Open a project with `cd path/to/project && vim README.md`. Press **Esc** before using the Vim keys below. The leader key is **comma**.

| In Vim or Neovim | What it does |
| --- | --- |
| `,f` / `,g` | Find a file / search the project with ripgrep. |
| `,b` / `,d` | Switch buffers / toggle the file tree. |
| `,w` / `:q` | Save / close the current window. |
| `:Git` | Open Git status through Fugitive. |
| `:Codex` | Start Codex in a terminal split in the current directory. |
| `:CodexResume` | Reopen the most recent Codex chat for this directory. |

To return from the terminal to your file, press **Ctrl-W p** in Vim. In Neovim, press **Ctrl-\\**, **Ctrl-N**, then **Ctrl-W p**. Run `nvim` when you want native LSP navigation. Use `gd` for definition, `gr` for references, and `ga` for code actions.

| At the shell | What it does |
| --- | --- |
| `tmux new -A -s dev` | Create or reattach to the dev session. |
| **Ctrl-B** then **-** / **_** | Split the tmux pane top/bottom or left/right. |
| **Ctrl-B** then **d** | Detach. Reattach with the same tmux command. |
| `codex resume --last` | Continue the last chat in this directory. |
| `codex review --uncommitted` | Review the working tree before committing. |

Inside Codex, type `/skills` to browse installed skills. Try `$dotfiles-check verify my installer changes` in this repo, or `$gh-fix-ci investigate the failing check` in a GitHub checkout. [Codex commands](https://developers.openai.com/codex/cli/slash-commands) · [Agent skills](https://developers.openai.com/codex/skills)

## Install on macOS

Run these from the checkout. Preview the destination files before replacing a customized profile.

```sh
git clone https://github.com/jxnl/dots.git
cd dots
brew bundle --file Brewfile
./install.sh --dry-run
./install.sh --backup
vim +PlugInstall
```

The installer copies the Vim and Neovim configs, Bash profile, tmux config, Claude/Codex/Cursor prompts, and Codex skills. With `--backup`, changed files get a timestamped sibling backup. Use `./install.sh --vim --backup` for just the editors or `./install.sh --skills --backup` for just the skills. Run `./install.sh --help` for all options.

For Neovim, run `:PlugInstall`, restart, then run `:TSInstall python lua vim go rust markdown` once. The Brewfile includes the parser compiler, Pyright, and gopls. If you use Rust through rustup, add its language server with `rustup component add rust-analyzer`.

The optional `.zshrc` template uses Oh My Zsh and loads NVM when installed. Keep machine-specific setup in your own profile. The installer leaves Zsh setup to you. The `gitignore` file is also a template.

## Verify a change

```sh
bash tests/run.sh
zsh -n .zshrc
brew bundle check --no-upgrade --file Brewfile
```
