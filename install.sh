#!/bin/bash
set -euo pipefail

# Default: install all components
INSTALL_VIM=true
INSTALL_BASH=true
INSTALL_TMUX=true
INSTALL_CLAUDE=true
INSTALL_OPENAI=true
INSTALL_CURSOR=true
INSTALL_CURSOR_PROJECT=false
INSTALL_SKILLS=false

SELECTED_PROMPTS=()
INTERACTIVE=false
DRY_RUN=false
BACKUP=false

is_tty() {
    [ -t 0 ] && [ -t 1 ]
}

prompt_yes_no() {
    local prompt="$1"
    local default="${2:-y}" # y|n
    local answer=""
    local suffix="[y/n]"
    if [ "$default" = "y" ]; then
        suffix="[Y/n]"
    elif [ "$default" = "n" ]; then
        suffix="[y/N]"
    fi

    while true; do
        printf "%s %s " "$prompt" "$suffix"
        read -r answer
        answer="$(echo "${answer:-}" | tr '[:upper:]' '[:lower:]' | xargs)"
        if [ -z "$answer" ]; then
            answer="$default"
        fi
        case "$answer" in
            y|yes) return 0 ;;
            n|no) return 1 ;;
        esac
        echo "Please enter y or n."
    done
}

backup_path() {
    local path="$1"
    local ts=""
    ts="$(date +"%Y%m%d-%H%M%S")"
    echo "${path}.bak.${ts}"
}

install_cp_file() {
    local src="$1"
    local dest="$2"
    if [ "$DRY_RUN" = true ]; then
        echo "[dry-run] cp \"$src\" \"$dest\""
        return 0
    fi
    if [ -e "$dest" ] && cmp -s "$src" "$dest"; then
        echo "Skipping $dest (identical)"
        return 0
    fi
    if [ "$BACKUP" = true ] && [ -e "$dest" ]; then
        local bak
        bak="$(backup_path "$dest")"
        cp -a "$dest" "$bak"
        echo "Backed up $dest -> $bak"
    fi
    cp "$src" "$dest"
}

install_cp_dir_contents() {
    local src_dir="$1"
    local dest_dir="$2"
    if [ "$DRY_RUN" = true ]; then
        echo "[dry-run] cp -r \"$src_dir/.\" \"$dest_dir/\""
        return 0
    fi
    mkdir -p "$dest_dir"
    cp -r "$src_dir/." "$dest_dir/"
}

list_prompts() {
    if [ -d "agents/prompts" ]; then
        find agents/prompts -maxdepth 1 -type f -name '*.md' -print \
            | xargs -n1 basename \
            | sed 's/\\.md$//' \
            | sort
    fi
}

require_prompt_exists() {
    local prompt="$1"
    if [ ! -f "agents/prompts/${prompt}.md" ]; then
        echo "Unknown prompt: ${prompt}"
        echo ""
        echo "Available prompts:"
        list_prompts | sed 's/^/  - /'
        exit 1
    fi
}

interactive_select_prompts() {
    local available=()
    local line=""
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        available+=("$line")
    done < <(list_prompts)

    if [ ${#available[@]} -eq 0 ]; then
        echo "No prompts found under agents/prompts."
        SELECTED_PROMPTS=()
        return 0
    fi

    echo ""
    echo "Prompt install options:"
    echo "  1) All prompts"
    echo "  2) Choose prompts"
    echo "  3) No prompts"
    echo ""

    local choice=""
    while true; do
        printf "Select an option [1-3]: "
        read -r choice
        choice="$(echo "${choice:-}" | xargs)"
        case "$choice" in
            1)
                SELECTED_PROMPTS=()
                return 0
                ;;
            2)
                echo ""
                echo "Available prompts:"
                local i=1
                for p in "${available[@]}"; do
                    printf "  %2d) %s\n" "$i" "$p"
                    i=$((i + 1))
                done
                echo ""
                echo "Enter numbers (comma-separated), e.g. 1,4,7"
                local nums=""
                printf "Selection: "
                read -r nums
                nums="$(echo "${nums:-}" | tr -d ' ' )"
                IFS=',' read -r -a _NUMS <<< "$nums"
                SELECTED_PROMPTS=()
                for n in "${_NUMS[@]}"; do
                    [ -z "$n" ] && continue
                    if ! [[ "$n" =~ ^[0-9]+$ ]]; then
                        echo "Invalid selection: $n"
                        SELECTED_PROMPTS=()
                        return 1
                    fi
                    if [ "$n" -lt 1 ] || [ "$n" -gt "${#available[@]}" ]; then
                        echo "Out of range: $n"
                        SELECTED_PROMPTS=()
                        return 1
                    fi
                    SELECTED_PROMPTS+=("${available[$((n - 1))]}")
                done
                for p in "${SELECTED_PROMPTS[@]}"; do
                    require_prompt_exists "$p"
                done
                return 0
                ;;
            3)
                SELECTED_PROMPTS=("__NONE__")
                return 0
                ;;
        esac
        echo "Please enter 1, 2, or 3."
    done
}

run_interactive_wizard() {
    if ! is_tty; then
        echo "Error: --interactive requires a TTY."
        exit 1
    fi

    echo "Interactive installer"
    echo ""

    INSTALL_VIM=false
    INSTALL_BASH=false
    INSTALL_TMUX=false
    INSTALL_CLAUDE=false
    INSTALL_OPENAI=false
    INSTALL_CURSOR=false
    INSTALL_CURSOR_PROJECT=false

    if prompt_yes_no "Install vim config (vimrc + colors)?" y; then INSTALL_VIM=true; fi
    if prompt_yes_no "Install bash config (bash_profile)?" y; then INSTALL_BASH=true; fi
    if prompt_yes_no "Install tmux config (tmux.conf)?" y; then INSTALL_TMUX=true; fi

    echo ""
    if prompt_yes_no "Install assistant prompts/configs?" y; then
        if prompt_yes_no "  Install Claude config?" y; then INSTALL_CLAUDE=true; fi
    if prompt_yes_no "  Install Codex config (OpenAI Developers)?" y; then INSTALL_OPENAI=true; fi
    if prompt_yes_no "  Install Codex skills?" y; then INSTALL_SKILLS=true; fi
        if prompt_yes_no "  Install Cursor commands (global)?" y; then INSTALL_CURSOR=true; fi
        if prompt_yes_no "  Install Cursor commands into this repo (.cursor/commands)?" n; then INSTALL_CURSOR_PROJECT=true; fi

        if [ "$INSTALL_CLAUDE" = true ] || [ "$INSTALL_OPENAI" = true ] || [ "$INSTALL_CURSOR" = true ] || [ "$INSTALL_CURSOR_PROJECT" = true ]; then
            interactive_select_prompts || exit 1
        fi
    fi

    echo ""
    if prompt_yes_no "Backup existing files before overwriting?" y; then BACKUP=true; fi
    if prompt_yes_no "Preview actions without changing anything (dry-run)?" n; then DRY_RUN=true; fi

    echo ""
    echo "Summary:"
    echo "  vim:            $INSTALL_VIM"
    echo "  bash:           $INSTALL_BASH"
    echo "  tmux:           $INSTALL_TMUX"
    echo "  claude:         $INSTALL_CLAUDE"
    echo "  codex(openai):  $INSTALL_OPENAI"
    echo "  cursor(global): $INSTALL_CURSOR"
    echo "  cursor(project):$INSTALL_CURSOR_PROJECT"
    echo "  codex skills:   $INSTALL_SKILLS"
    echo "  backup:         $BACKUP"
    echo "  dry-run:        $DRY_RUN"
    if [ ${#SELECTED_PROMPTS[@]} -gt 0 ]; then
        if [ "${SELECTED_PROMPTS[0]}" = "__NONE__" ]; then
            echo "  prompts:        none"
        elif [ "${#SELECTED_PROMPTS[@]}" -gt 0 ]; then
            echo "  prompts:        ${SELECTED_PROMPTS[*]}"
        fi
    fi
    echo ""
    if ! prompt_yes_no "Proceed?" y; then
        echo "Aborted."
        exit 0
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --interactive)
            INTERACTIVE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --backup)
            BACKUP=true
            shift
            ;;
        --vim)
            INSTALL_VIM=true
            INSTALL_BASH=false
            INSTALL_TMUX=false
            INSTALL_CLAUDE=false
            INSTALL_OPENAI=false
            INSTALL_CURSOR=false
            INSTALL_CURSOR_PROJECT=false
            shift
            ;;
        --bash)
            INSTALL_VIM=false
            INSTALL_BASH=true
            INSTALL_TMUX=false
            INSTALL_CLAUDE=false
            INSTALL_OPENAI=false
            INSTALL_CURSOR=false
            INSTALL_CURSOR_PROJECT=false
            shift
            ;;
        --tmux)
            INSTALL_VIM=false
            INSTALL_BASH=false
            INSTALL_TMUX=true
            INSTALL_CLAUDE=false
            INSTALL_OPENAI=false
            INSTALL_CURSOR=false
            INSTALL_CURSOR_PROJECT=false
            shift
            ;;
        --agents)
            INSTALL_VIM=false
            INSTALL_BASH=false
            INSTALL_TMUX=false
            INSTALL_CLAUDE=true
            INSTALL_OPENAI=true
            INSTALL_CURSOR=true
            INSTALL_CURSOR_PROJECT=false
            INSTALL_SKILLS=true
            shift
            ;;
        --claude)
            INSTALL_VIM=false
            INSTALL_BASH=false
            INSTALL_TMUX=false
            INSTALL_CLAUDE=true
            INSTALL_OPENAI=false
            INSTALL_CURSOR=false
            INSTALL_CURSOR_PROJECT=false
            shift
            ;;
        --openai|--codex)
            INSTALL_VIM=false
            INSTALL_BASH=false
            INSTALL_TMUX=false
            INSTALL_CLAUDE=false
            INSTALL_OPENAI=true
            INSTALL_CURSOR=false
            INSTALL_CURSOR_PROJECT=false
            INSTALL_SKILLS=false
            shift
            ;;
        --cursor)
            INSTALL_VIM=false
            INSTALL_BASH=false
            INSTALL_TMUX=false
            INSTALL_CLAUDE=false
            INSTALL_OPENAI=false
            INSTALL_CURSOR=true
            INSTALL_CURSOR_PROJECT=false
            shift
            ;;
        --cursor-project)
            INSTALL_VIM=false
            INSTALL_BASH=false
            INSTALL_TMUX=false
            INSTALL_CLAUDE=false
            INSTALL_OPENAI=false
            INSTALL_CURSOR=false
            INSTALL_CURSOR_PROJECT=true
            INSTALL_SKILLS=false
            shift
            ;;
        --skills)
            INSTALL_VIM=false
            INSTALL_BASH=false
            INSTALL_TMUX=false
            INSTALL_CLAUDE=false
            INSTALL_OPENAI=false
            INSTALL_CURSOR=false
            INSTALL_CURSOR_PROJECT=false
            INSTALL_SKILLS=true
            shift
            ;;
        --prompt)
            if [ -z "$2" ]; then
                echo "Missing value for --prompt"
                exit 1
            fi
            require_prompt_exists "$2"
            SELECTED_PROMPTS+=("$2")
            shift 2
            ;;
        --only-prompts)
            if [ -z "$2" ]; then
                echo "Missing value for --only-prompts"
                exit 1
            fi
            IFS=',' read -r -a _PROMPTS <<< "$2"
            for p in "${_PROMPTS[@]}"; do
                p="$(echo "$p" | xargs)"
                [ -z "$p" ] && continue
                require_prompt_exists "$p"
                SELECTED_PROMPTS+=("$p")
            done
            shift 2
            ;;
        --list-prompts)
            list_prompts
            exit 0
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --interactive  Interactive installer (prompts for choices)"
            echo "  --backup  Backup existing destination files before overwriting"
            echo "  --dry-run  Print actions without writing files"
            echo "  --vim     Install only vim configuration"
            echo "  --bash    Install only bash configuration"
            echo "  --tmux    Install only tmux configuration"
            echo "  --agents  Install assistant prompts (Claude + Codex + Cursor)"
            echo "  --claude  Install only Claude configuration"
            echo "  --openai/--codex  Install only Codex configuration (OpenAI Developers)"
            echo "  --cursor  Install only Cursor commands (global)"
            echo "  --cursor-project  Install Cursor commands to .cursor/commands (project)"
            echo "  --skills  Install Codex skills to ~/.codex/skills"
            echo "  --prompt NAME  Install only one prompt (repeatable)"
            echo "  --only-prompts a,b,c  Install only these prompts"
            echo "  --list-prompts  List available prompts"
            echo "  --help    Show this help message"
            echo ""
            echo "Default: Install all components"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

if [ "$INTERACTIVE" = true ]; then
    run_interactive_wizard
fi

if [ ${#SELECTED_PROMPTS[@]} -gt 0 ] && [ "$INSTALL_CLAUDE" != true ] && [ "$INSTALL_OPENAI" != true ] && [ "$INSTALL_CURSOR" != true ] && [ "$INSTALL_CURSOR_PROJECT" != true ]; then
    echo "Warning: --prompt/--only-prompts has no effect unless installing prompts for Claude/Codex/Cursor." >&2
fi

echo "Installing dotfiles..."

# Install vim configuration
if [ "$INSTALL_VIM" = true ]; then
    echo "📝 Installing vim configuration..."
    mkdir -p ~/.vim
    install_cp_file vimrc ~/.vimrc
    if [ "$DRY_RUN" = true ]; then
        echo "[dry-run] cp -r \"colors\" \"$HOME/.vim/\""
    else
        if [ "$BACKUP" = true ] && [ -e "$HOME/.vim/colors" ]; then
            bak="$(backup_path "$HOME/.vim/colors")"
            cp -a "$HOME/.vim/colors" "$bak"
            echo "Backed up $HOME/.vim/colors -> $bak"
        fi
        cp -r colors ~/.vim/
    fi
    echo "✅ Vim configuration installed"
fi

# Install bash configuration
if [ "$INSTALL_BASH" = true ]; then
    echo "🐚 Installing bash configuration..."
    install_cp_file bash_profile ~/.bash_profile
    echo "✅ Bash configuration installed"
fi

# Install tmux configuration
if [ "$INSTALL_TMUX" = true ]; then
    echo "🖥️  Installing tmux configuration..."
    install_cp_file tmux.conf ~/.tmux.conf
    echo "✅ Tmux configuration installed"
fi

# Install Claude configuration
if [ "$INSTALL_CLAUDE" = true ]; then
    echo "🤖 Installing Claude configuration..."
    mkdir -p ~/.claude/commands
    install_cp_file agents/AGENTS.md ~/.claude/CLAUDE.md
    if [ ${#SELECTED_PROMPTS[@]} -gt 0 ] && [ "${SELECTED_PROMPTS[0]}" = "__NONE__" ]; then
        : # no prompts
    elif [ ${#SELECTED_PROMPTS[@]} -gt 0 ]; then
        for prompt in "${SELECTED_PROMPTS[@]}"; do
            install_cp_file "agents/prompts/${prompt}.md" ~/.claude/commands/"${prompt}.md"
        done
    else
        install_cp_dir_contents agents/prompts ~/.claude/commands
    fi
    echo "✅ Claude configuration installed"
fi

if [ "$INSTALL_OPENAI" = true ]; then
    echo "🧠 Installing Codex configuration (OpenAI Developers)..."
    mkdir -p ~/.codex/prompts
    if [ ${#SELECTED_PROMPTS[@]} -gt 0 ] && [ "${SELECTED_PROMPTS[0]}" = "__NONE__" ]; then
        : # no prompts
    elif [ ${#SELECTED_PROMPTS[@]} -gt 0 ]; then
        for prompt in "${SELECTED_PROMPTS[@]}"; do
            install_cp_file "agents/prompts/${prompt}.md" ~/.codex/prompts/"${prompt}.md"
        done
    else
        install_cp_dir_contents agents/prompts ~/.codex/prompts
    fi
    echo "✅ Codex configuration installed"
fi

if [ "$INSTALL_SKILLS" = true ]; then
    echo "🧠 Installing Codex skills..."
    mkdir -p ~/.codex/skills
    if [ -d "agents/skills" ]; then
        install_cp_dir_contents agents/skills ~/.codex/skills
    else
        echo "No skills found under agents/skills."
    fi
    echo "✅ Codex skills installed"
fi

if [ "$INSTALL_CURSOR" = true ]; then
    echo "🧭 Installing Cursor commands..."
    mkdir -p ~/.cursor/commands
    if [ ${#SELECTED_PROMPTS[@]} -gt 0 ] && [ "${SELECTED_PROMPTS[0]}" = "__NONE__" ]; then
        : # no prompts
    elif [ ${#SELECTED_PROMPTS[@]} -gt 0 ]; then
        for prompt in "${SELECTED_PROMPTS[@]}"; do
            install_cp_file "agents/prompts/${prompt}.md" ~/.cursor/commands/"${prompt}.md"
        done
    else
        install_cp_dir_contents agents/prompts ~/.cursor/commands
    fi
    echo "✅ Cursor commands installed"
fi

if [ "$INSTALL_CURSOR_PROJECT" = true ]; then
    echo "🧭 Installing Cursor project commands..."
    mkdir -p .cursor/commands
    if [ ${#SELECTED_PROMPTS[@]} -gt 0 ] && [ "${SELECTED_PROMPTS[0]}" = "__NONE__" ]; then
        : # no prompts
    elif [ ${#SELECTED_PROMPTS[@]} -gt 0 ]; then
        for prompt in "${SELECTED_PROMPTS[@]}"; do
            install_cp_file "agents/prompts/${prompt}.md" .cursor/commands/"${prompt}.md"
        done
    else
        install_cp_dir_contents agents/prompts .cursor/commands
    fi
    echo "✅ Cursor project commands installed"
fi

echo ""
echo "🎉 Installation complete!"
if [ "$INSTALL_VIM" = true ]; then
    echo "📝 Don't forget to run :PlugInstall in vim/nvim"
fi
