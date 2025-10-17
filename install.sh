#!/bin/bash

# Default: install all components
INSTALL_VIM=true
INSTALL_BASH=true
INSTALL_TMUX=true
INSTALL_CLAUDE=true

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --vim)
            INSTALL_VIM=true
            INSTALL_BASH=false
            INSTALL_TMUX=false
            INSTALL_CLAUDE=false
            shift
            ;;
        --bash)
            INSTALL_VIM=false
            INSTALL_BASH=true
            INSTALL_TMUX=false
            INSTALL_CLAUDE=false
            shift
            ;;
        --tmux)
            INSTALL_VIM=false
            INSTALL_BASH=false
            INSTALL_TMUX=true
            INSTALL_CLAUDE=false
            shift
            ;;
        --claude)
            INSTALL_VIM=false
            INSTALL_BASH=false
            INSTALL_TMUX=false
            INSTALL_CLAUDE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --vim     Install only vim configuration"
            echo "  --bash    Install only bash configuration"
            echo "  --tmux    Install only tmux configuration"
            echo "  --claude  Install only Claude configuration"
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
    cp -r claude ~/.claude
    echo "✅ Claude configuration installed"
fi

echo ""
echo "🎉 Installation complete!"
if [ "$INSTALL_VIM" = true ]; then
    echo "📝 Don't forget to install Vundle and run :BundleInstall in vim"
fi
