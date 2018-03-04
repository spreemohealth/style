#!/usr/bin/env bash

# get installer's parent directory
INSTALLER_DIR=$(dirname $(realpath $0))

# get target repository
REPO_PATH=$1

# copy files in the REPO_PATHsitory hooks subdirectory
cp $INSTALLER_DIR/py/py_flake8.py $REPO_PATH/.git/hooks
chmod +x $REPO_PATH/.git/hooks/py_flake8.py

cp $INSTALLER_DIR/r/r_lintr.R $REPO_PATH/.git/hooks
cp $INSTALLER_DIR/r/r_lintr.sh $REPO_PATH/.git/hooks
chmod +x $REPO_PATH/.git/hooks/r_lintr.sh

cp $INSTALLER_DIR/pre-commit $REPO_PATH/.git/hooks
chmod +x $REPO_PATH/.git/hooks/pre-commit