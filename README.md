# What is this?
This repository contains code used to manage and enforce style/code checking in the `spreemohealth` GitHub organization.

## Configuring a pre-commit hook
This section explains how to configure a client-level pre-commit hook.

Currently, this hook performs code checking on your commits for the following languages:
- Python, using `flake8`
- R, using `lintr`.

If you try to commit code that does pass the check, your commit is rejected.
In that case, fix your code and commit again.

1. Please make sure that `coreutils` is installed on your system:
   ```bash
   brew install coreutils
   ```

2. Clone this repository on your system (say in `~/Git/style`).

3. Make the installer executable:
   ```bash
   chmod +x ~/Git/style/client/installer.sh
   ```

4. Run the installer on the desired repository (e.g. on `~/Git/my-linty-repo`)
   ```bash
   ./~/Git/style/client/installer.sh ~/Git/my-linty-repo
   ```

5. You are all set.
