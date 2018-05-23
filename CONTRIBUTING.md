# Contributing to `spreemohealth/style`

We are very happy to receive Pull Requests!

If you decide to contribute, please follow these general guidelines.

## How to contribute

1. Fork this repository.

2. Make your edits/additions.

3. Add meaningful tests for your code.

4. When you are done with your work, open a Pull Request (please set
   `base: staging` in your PR).
   The PR will trigger a build on CircleCI.
   If the build is not successful, please make the necessary edits.

5. We will reach out if we feel that changes are needed or if we have other
   feedback.
   Otherwise, we will merge the PR into `staging` and close the PR.

We periodically review the contents of the `staging` branch, merge it into
`master`, and [release a new version of the `style` repository](https://github.com/spreemohealth/style/releases).

## Adding support for additional linters

If you add support for additional linters, please

- subclass from the `Linter` class defined in
  [`pre_commit.linters`](https://github.com/spreemohealth/style/blob/master/pre_commit/linters.py)
  whenever possible

- update the `install.py` file

- update the `README.md` file

- update the `pre_commit/uninstall.py` file, if needed.
