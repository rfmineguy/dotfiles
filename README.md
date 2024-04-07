# dotfiles
A home for my MacOS/Linux dotfiles to live

# description
This is a place where I store my dotfiles and their corresponding installation script.
The installation is done via the `link.py` python script. It is highly recommended to look through it for yourself to ensure that it doesn't do anything unintended.
I am confident that it wont harm anything, but you should **ALWAYS** make sure for yourself

The way it works is that it symbolically links the folders/files in **this** directory to the appropriate configuration directories specified in the `link.py` script.

# usage

```sh
Usage:
  $ python3 link.py create --target <target>     # creates symlink for target based on linkdir in script
  $ python3 link.py remove --target <target>     # removes symlink for the target (effectively uninstalling the configuration)
  $ python3 link.py getlinkdir --target <target> # prints out where the target would get linked has create been run instead

Targets:
  nvim    # linkdir in link.py
  qtile   # linkdir in link.py
  tmux    # linkdir in link.py
```
