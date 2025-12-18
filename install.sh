#!/bin/bash

# Default: install all components
INSTALL_VIM=true
INSTALL_BASH=true
INSTALL_TMUX=true
INSTALL_CLAUDE=true
INSTALL_OPENAI=true
INSTALL_CURSOR=true
INSTALL_CURSOR_PROJECT=false

SELECTED_PROMPTS=()

list_prompts() {
    if [ -d "agents/prompts" ]; then
        ls -1 agents/prompts/*.md 2>/dev/null | xargs -n1 basename | sed 's/\\.md$//' | sort
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

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
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
            echo "  --vim     Install only vim configuration"
            echo "  --bash    Install only bash configuration"
            echo "  --tmux    Install only tmux configuration"
            echo "  --agents  Install assistant prompts (Claude + Codex)"
            echo "  --claude  Install only Claude configuration"
            echo "  --openai  Install only Codex configuration (OpenAI Developers)"
            echo "  --cursor  Install only Cursor commands (global)"
            echo "  --cursor-project  Install Cursor commands to .cursor/commands (project)"
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

if [ ${#SELECTED_PROMPTS[@]} -gt 0 ] && [ "$INSTALL_CLAUDE" != true ] && [ "$INSTALL_OPENAI" != true ] && [ "$INSTALL_CURSOR" != true ] && [ "$INSTALL_CURSOR_PROJECT" != true ]; then
    echo "Warning: --prompt/--only-prompts has no effect unless installing prompts for Claude/Codex/Cursor." >&2
fi

echo "Installing dotfiles..."

# Install vim configuration
if [ "$INSTALL_VIM" = true ]; then
    echo "📝 Installing vim configuration..."
    mkdir -p ~/.vim
    cp vimrc ~/.vimrc
    cp -r colors ~/.vim/
    echo "✅ Vim configuration installed"
fi

# Install bash configuration
if [ "$INSTALL_BASH" = true ]; then
    echo "🐚 Installing bash configuration..."
    cp bash_profile ~/.bash_profile
    echo "✅ Bash configuration installed"
fi

# Install tmux configuration
if [ "$INSTALL_TMUX" = true ]; then
    echo "🖥️  Installing tmux configuration..."
    cp tmux.conf ~/.tmux.conf
    echo "✅ Tmux configuration installed"
fi

# Install Claude configuration
if [ "$INSTALL_CLAUDE" = true ]; then
    echo "🤖 Installing Claude configuration..."
    mkdir -p ~/.claude/commands
    cp agents/AGENTS.md ~/.claude/CLAUDE.md
    cp agents/claude/settings.json ~/.claude/settings.json
    if [ ${#SELECTED_PROMPTS[@]} -gt 0 ]; then
        for prompt in "${SELECTED_PROMPTS[@]}"; do
            cp "agents/prompts/${prompt}.md" ~/.claude/commands/
        done
    else
        cp -r agents/prompts/. ~/.claude/commands/
    fi
    echo "✅ Claude configuration installed"
fi

if [ "$INSTALL_OPENAI" = true ]; then
    echo "🧠 Installing Codex configuration (OpenAI Developers)..."
    mkdir -p ~/.codex/prompts
    if [ ${#SELECTED_PROMPTS[@]} -gt 0 ]; then
        for prompt in "${SELECTED_PROMPTS[@]}"; do
            cp "agents/prompts/${prompt}.md" ~/.codex/prompts/
        done
    else
        cp -r agents/prompts/. ~/.codex/prompts/
    fi
    echo "✅ Codex configuration installed"
fi

if [ "$INSTALL_CURSOR" = true ]; then
    echo "🧭 Installing Cursor commands..."
    mkdir -p ~/.cursor/commands
    if [ ${#SELECTED_PROMPTS[@]} -gt 0 ]; then
        for prompt in "${SELECTED_PROMPTS[@]}"; do
            cp "agents/prompts/${prompt}.md" ~/.cursor/commands/
        done
    else
        cp -r agents/prompts/. ~/.cursor/commands/
    fi
    echo "✅ Cursor commands installed"
fi

if [ "$INSTALL_CURSOR_PROJECT" = true ]; then
    echo "🧭 Installing Cursor project commands..."
    mkdir -p .cursor/commands
    if [ ${#SELECTED_PROMPTS[@]} -gt 0 ]; then
        for prompt in "${SELECTED_PROMPTS[@]}"; do
            cp "agents/prompts/${prompt}.md" .cursor/commands/
        done
    else
        cp -r agents/prompts/. .cursor/commands/
    fi
    echo "✅ Cursor project commands installed"
fi

echo ""
echo "🎉 Installation complete!"
if [ "$INSTALL_VIM" = true ]; then
    echo "📝 Don't forget to install Vundle and run :BundleInstall in vim"
fi
