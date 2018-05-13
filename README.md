# Style

> You got that James Dean daydream look in your eye
>
> And I got that red lip, classic thing that you like
>
> And when we go crashing down, we come back every time
>
> 'Cause we never go out of style, we never go out of style...

![style](http://teenageoracle.weebly.com/uploads/5/0/3/4/50348443/ezgif-2-9e4c6f0617_orig.gif)

## Purpose of this repository

`style` is a small repository designed to encourage style and code checking.

"But why?", you ask.

The short answer is code maintainability (although maintainability is not the
only reason why you should
[lint](https://en.wikipedia.org/wiki/Lint_(software))
your code).

You'll find many articles on the web discussing the advantages of code linting.
For example:

> Reading code written in an unfamiliar style is like reading poor handwriting.
> The information is all there, but it requires inordinate concentration
> simply to extract to it. Conversely, reading code that adheres to a familiar
> style allows you to focus on what is important.
> Whether it’s someone else’s code or your own that you are returning to,
> having a common style greatly reduces maintainability costs.

(source: <https://blog.adeptmarketing.com/how-linting-produces-better-code>).

`style` allows you to easily install a pre-commit git hook in your local git
repositories.

The hook works as follows:

1. You commit your code.
2. A series of linters are run on your code.
3. If the linters find that there is something wrong with your code,
   your commit is rejected. In this case, simply make the appropriate edits
   and commit again.

## Languages

Currently, `style` performs code checking on file written in

- **Markdown** (`.md` files), using
  [`markdownlint`](https://github.com/igorshubovych/markdownlint-cli)

- **Python** (`.py` files), using
  [`flake8`](https://github.com/PyCQA/flake8)

- **R** (`.r` or `.R` files), using
  [`lintr`](https://github.com/jimhester/lintr).

## Installing the pre-commit hook

1. Please make sure that Python 3 and R are both installed on your system.

   *Note that in this example, `python` and `pip` point to my Homebrew*
   *Python 3 distribution.*
   *If you are using a different distribution, please make the appropriate*
   *changes in the commands that follow.*

2. Make sure that the following are installed on your system:

   - `markdownlint-cli`:
      ```bash
      npm install -g markdownlint-cli
      ```

   - the Python `flake8` module (for Python 3):
      ```bash
      pip install flake8 --upgrade
      ```

   - the R `lintr` package:
      ```bash
      R -e "install.packages('lintr', repos='https://cloud.r-project.org')"
      ```

3. Clone this repository on your system (say in `~/Git/style`) and `cd`
   into it.

4. Run the installer on the target repository (e.g. `~/Git/my-linty-repo` in
   the following example):

   ```bash
   python install ~/Git/my-linty-repo
   ```

   If you want, you can perform the installation on more than one target
   repository:

   ```bash
   python install ~/Git/my-linty-repo ~/Git/my-linty-repo2 ...
   ```

   By default, the installation activates all available linters.
   Alternatively, you can select which linters you want to activate by means
   of short flags.

   For instance, in order to activate only the Python linter
   in `~/Git/my-linty-repo` you can run

   ```bash
   python install -p ~/Git/my-linty-repo
   ```

   or, to activate the Markdown and the Python linter, but not the R linter,
   you can run

   ```bash
   python install -m -p ~/Git/my-linty-repo
   ```

   or

   ```bash
   python install -mp ~/Git/my-linty-repo
   ```

## Uninstalling the pre-commmit hook

1. `cd` into the root of the repository, e.g.

   ```bash
   cd ~/Git/my-linty-repo
   ```

2. Run the `uninstall.py` script in `.git/hooks/pre_commit` with

   ```bash
   python .git/hooks/pre_commit/uninstall.py
   ```

## Adding support for more linters

You can leverage the `Linter` class in
[`pre_commit.linters`](https://github.com/spreemohealth/style/blob/master/pre_commit/linters.py)
to add support for a variety of additional linters.

## Contributing to this repository

Please refer to the
[CONTRINUTING.md](https://github.com/spreemohealth/style/blob/master/CONTRIBUTING.md)
file for instructions on how to contribute to this repository.

## How to avoid code checking

Generally, you want *all* of your code to be checked without exceptions.
However, there may be special circumstances under which you may desire to
exclude a line or a block of code from being checked.

This section illustrates some ways of selectively excluding portions of your
code from being checked.
Please refer to the documentation of the relevant packages for more details.

**Use wisely!**

![shudders](https://media.giphy.com/media/3orieQK00Z7KbsPvnG/giphy.gif)

### Markdown - `markdownlint`

Code in a block like this one

```markdown
<!-- markdownlint-disable -->
...CODE...
<!-- markdownlint-enable -->
```

is not checked.

You can exclude specific errors (`MD001` and `MD002` in the example that
follows) with:

```markdown
<!-- markdownlint-disable MD001 MD002 -->
...CODE...
<!-- markdownlint-enable MD001 MD002 -->
```

### Python - `flake8`

You can exclude an entire file from being checked by including the following
line at the top of it:

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

You can exclude specific errors on a line with `# noqa: <error>`,
e.g. `# noqa: E234`.

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

## Useful links

- [`markdownlint`'s Markdown style guide](https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md)

- [Python's PEP8 (official)](http://pep8.org);
  [Python's PEP8 (easier to read)](https://www.python.org/dev/peps/pep-0008/)

- [Hadley's R style guide](http://r-pkgs.had.co.nz/style.html)
