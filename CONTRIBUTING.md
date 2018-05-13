# Contributing to `spreemohealth/style`

We are very happy to receive Pull Requests!

Here are some guidelines.

## How to contribute

1. Fork the repository and add your code / make your edits in a branch of
   your own.

2. Please add tests.

3. Pushing your changes to your own branch will trigger a build on CircleCI.

4. When you are done with your work and the build on CircleCI is successful,
   open a Pull Request from your branch into `staging`.

5. We will reach out if we feel changes are needed or if we have other
   feedback.
   Otherwise, we will merge the PR into `staging` and delete your remote
   branch.

## Adding support for additional linters

If you add support for additional linters, please

- subclass from the `Linter` class defined in
  [`pre_commit.linters`](https://github.com/spreemohealth/style/blob/master/pre_commit/linters.py)
  whenever possible

- update the `style/install.py` file

- update the `style/uninstall.py` file.
