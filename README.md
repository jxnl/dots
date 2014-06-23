.vimrc
--------

Clone this repo and `mv /vim-files/.vimrc ~`.

To install Vundle:
  
    $ git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle

Some bits inspired by https://github.com/amix/vimrc/blob/master/vimrcs/extended.vim


# Notes:

Here are some added features that I have installed. And a short summary of what it does.

*Easymotion*

This is a bundle I've started using to move quickly between lines. To start, press `\\` followed by `w` or any of the motion keys.
What this will do is highlight words you can jump to by pressing a single letter or `;` followed by a letter

@todo, add sample image.

*Python Docs*

This is cool if you code in python. If you have your cursor over some python functions or what not, if you press `K` you will open a split
that shows you the documentation of the function


*Gundo*

Make some edits, make some mistakes. Want to see all your undo history? Press `<f5>`!!!
It shows you diffs, magic I know.

*Files on Files on Files*

My vimrc also loves tabs and directory trees. Type `:Nerdtree` in vim and you'll see al your files.
If you want to go faster, experiment with `\f` or `\n` to jump around files. I have a most recently used tab at the top 
if you need to jump around more. More on that, `w+[hjkl]` is all you need to move from screen to screen.

