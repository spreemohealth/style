#!/usr/bin/env bash

# get path to target repository
repo=$1

# install lintr, if not already installed
if ! Rscript --vanilla -e "library(lintr)" &> /dev/null ; then
    Rscript --vanilla -e "install.packages('lintr', repos = 'https://cloud.r-project.org')"
fi

# add the R lintr utility script
cp ./client/r/r_lintr.R $repo/.git/hooks/

# add the hook as .git/hooks/pre-commit
cp ./client/r/r_lintr.sh $repo/.git/hooks/pre-commit
chmod +x $repo/.git/hooks/pre-commit
