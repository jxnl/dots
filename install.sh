#!/bin/bash

echo "Installing dotfiles..."

# Create necessary directories
mkdir -p ~/.vim

# Copy configuration files
cp vimrc ~/.vimrc
cp bash_profile ~/.bash_profile
cp tmux.conf ~/.tmux.conf
cp -r colors ~/.vim/
cp -r claude ~/.claude

echo "✅ Dotfiles installed successfully!"
echo "📝 Don't forget to install Vundle and run :BundleInstall in vim"
