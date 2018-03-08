#!/usr/bin/env bash

# get installer's parent directory
INSTALLER_DIR=$(dirname $(realpath $0))

# get target repository
REPO_PATH=$1

# make a 'style' directory in .git/hooks
mkdir -p $REPO_PATH/.git/hooks/style

# copy files in the REPO_PATH hooks subdirectory
cp $INSTALLER_DIR/util.sh $REPO_PATH/.git/hooks/style

cp $INSTALLER_DIR/py/py_flake8.sh $REPO_PATH/.git/hooks/style
chmod +x $REPO_PATH/.git/hooks/style/py_flake8.sh

cp $INSTALLER_DIR/r/r_lintr.sh $REPO_PATH/.git/hooks/style
chmod +x $REPO_PATH/.git/hooks/style/r_lintr.sh

cp $INSTALLER_DIR/pre-commit $REPO_PATH/.git/hooks
chmod +x $REPO_PATH/.git/hooks/pre-commit