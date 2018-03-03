#!/usr/bin/env bash

# install required R dependencies
R CMD -e "install.packages(c('lintr', 'littlr'), repos = 'https://cloud.r-project.org'"

# add the R lintr utility script
cp r_lintr.R ./.git/hooks/

# add the hook as .git/hooks/pre-commit
cp r_lintr.sh ./.git/hooks/pre-commit