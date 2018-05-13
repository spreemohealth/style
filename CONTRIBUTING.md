# Contributing to `spreemohealth/style`

We are very happy to receive Pull Requests!

Here are some guidelines.

## How to contribute

1. Fork the repository.

2. Branch from `staging` and add your code / make your edits in your own
   branch.

3. Add meaningful tests for your code additions.

4. Push your changes to your own branch to trigger a build on CircleCI.

5. When you are done with your work and the build on CircleCI is successful,
   open a Pull Request from your branch into `staging`.

6. We will reach out if we feel changes are needed or if we have other
   feedback.
   Otherwise, we will merge the PR into `staging` and delete your remote
   branch.

We periodically review the contents of the `staging` branch and merge the
`staging` branch into the master branch.
These "releases" are documented in the
[`RELEASES.md`](https://github.com/spreemohealth/style/blob/master/RELEASES.md)
file.

## Adding support for additional linters

If you add support for additional linters, please

- subclass from the `Linter` class defined in
  [`pre_commit.linters`](https://github.com/spreemohealth/style/blob/master/pre_commit/linters.py)
  whenever possible

- update the `install.py` file

- update the `pre_commit/uninstall.py` file

- update the `README.md` file.
