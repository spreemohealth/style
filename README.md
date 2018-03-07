# Style
> You got that James Dean daydream look in your eye
>
> And I got that red lip, classic thing that you like
>
> And when we go crashing down, we come back every time
>
> 'Cause we never go out of style, we never go out of style...

# What is this?
This repository contains code used to manage and enforce style/code checking in the `spreemohealth` GitHub organization.

## Configuring a pre-commit hook
**This section explains how to configure a client-level pre-commit hook for a target Git repository.**

---

Currently, this hook performs code checking on your commits for the following languages:
- **Python** (i.e. `.py` files), using `flake8`
- **R** (i.e. `.r` or `.R` files), using `lintr`.

---

In short, the hook works as follows: *if you commit code that does not pass the inspection, your commit will be rejected.*
When this happens, simply make the appropriate edits to your code and commit again.

1. Please make sure that `coreutils` is installed on your system:
   ```bash
   brew install coreutils
   ```

2. Make sure that `flake8` is available to the Python interpreter that you plan to use with the target repository:
   ```bash
   pip install flake8 --upgrade
   ```

3. Make sure that the R `lintr` package is installed:
   ```bash
   R -e "install.packages('lintr', repos='https://cloud.r-project.org')"
   ```

4. Clone this repository on your system (say in `~/Git/style`).

5. Make the installer executable:
   ```bash
   chmod +x ~/Git/style/client/installer.sh
   ```

6. Run the installer on the target repository (e.g. `~/Git/my-linty-repo` in the following example):
   ```bash
   ~/Git/style/client/installer.sh ~/Git/my-linty-repo
   ```

7. Your pre-commit hook should now be correctly configured on the target repository.

## How to avoid code checking
Generally, you want *all* of your code to be checked without exceptions.
However, there may be special circumstances under which you may desire to exclude a line or a block of code from being checked.
This section explains how to do this for the supported languages (more details can be found in the documentation of the relevant packages).

**Use wisely.**

### Python - `flake8`
You can exclude an entire file from being checked by including the following line at the top of it:
```python
# flake8: noqa
```

Use the `# noqa` inline comment to exclude a single line:
```python
# this line will raise an error
a= 1 

# this line will not raise an error,
# because it is excluded from code checking
b =2 # noqa
```

You can exclude specific errors on a line with `# noqa: <error>`, e.g. `# noqa: E234`.

### R - `lintr`
Use the `# nolint` inline comment to exclude a given line:
```R
# this line will raise an error
a= 1

# this line will not raise an error,
# because it is excluded from code checking
b =2 # nolint
```

You can exclude an entire block of code like so:
```R
# the following block will not raise errors
# because it is excluded from code checking

# nolint start
a= 1
b =2
# nolint end

# this line will raise an error
x <- c(1,2, 3)
```
