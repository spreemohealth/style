# What is this?
This repository contains code used to manage and enforce style/code checking in the `spreemohealth` GitHub organization.

## Python

### Configuring a flake8 pre-commit hook
1. `cd` into the root of your local repository
   ```bash
   cd ~/mattiaciollaro/Git/my_tidy_repo
   ```

2. activate your Python virtual environment, if one is configured for this project

3. run the configuration script
   ```bash
   source .../style/client/py_flake8_pre_commit
   ```

From now on, `flake8` will check your Python code against coding style (PEP8), programming errors, etc.
If `flake8` has non-zero exit status after checking your Python code, your commit will not be accepted: in this case, fix your code before committing your changes. 
