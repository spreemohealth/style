#!/bin/bash

# install style
python3 /style/install.py /repo/ >/dev/null 2>&1

# ask for git username and email
read -p 'git username: ' gituser
read -p 'git email: ' gitemail

# git configuration
git config --global user.name "$gituser"
git config --global user.email "$gitemail"

# define cleanup procedure
cleanup() {
    python3 /repo/.git/hooks/pre_commit/uninstall.py /repo/ >/dev/null 2>&1
}

# trap SIGTERM
trap 'true' SIGTERM

# launch a new shell
/bin/bash

# wait
wait $!

# cleanup
cleanup
