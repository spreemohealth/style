# What is this?
This repository contains code used to manage and enforce style/code checking in the `spreemohealth` GitHub organization.

## Configuring a pre-commit hook
This section explains how to configure a client-level pre-commit hook.

Currently, this hook performs code checking on your commits for the following languages:
- Python, using `flake8`
- R, using `lintr`.

If you commit code that does not pass the inspection, your commit will be rejected.
If this happens, simply make the appropriate edits to your code and commit again.

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
   ~/Git/style/client/installer.sh ~/Git/my-linty-repo
   ```

5. If this is a brand new repository, i.e. if there are no references in
   ```bash
   ~/Git/my-linty-repo/.git/refs/heads/master
   ```
   then please make a first "Initial commit" that does not involve code that should be checked (e.g. create a `README`, `.gitignore`, ...).

6. Your pre-commit hook should now be correctly configured.
