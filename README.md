# pygeosimplify

[![Release](https://img.shields.io/github/v/release/jbeirer/pygeosimplify)](https://img.shields.io/github/v/release/jbeirer/pygeosimplify)
[![Build status](https://img.shields.io/github/actions/workflow/status/jbeirer/pygeosimplify/main.yml?branch=main)](https://github.com/jbeirer/pygeosimplify/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/jbeirer/pygeosimplify/branch/main/graph/badge.svg)](https://codecov.io/gh/jbeirer/pygeosimplify)
[![Commit activity](https://img.shields.io/github/commit-activity/m/jbeirer/pygeosimplify)](https://img.shields.io/github/commit-activity/m/jbeirer/pygeosimplify)
[![License](https://img.shields.io/github/license/jbeirer/pygeosimplify)](https://img.shields.io/github/license/jbeirer/pygeosimplify)

This is a template repository for Python projects that use Poetry for their dependency management.

- **Github repository**: <https://github.com/jbeirer/pygeosimplify/>
- **Documentation** <https://jbeirer.github.io/pygeosimplify/>

## Getting started with your project

First, create a repository on GitHub with the same name as this project, and then run the following commands:

``` bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:jbeirer/pygeosimplify.git
git push -u origin main
```

Finally, install the environment and the pre-commit hooks with

```bash
make install
```

You are now ready to start development on your project! The CI/CD
pipeline will be triggered when you open a pull request, merge to main,
or when you create a new release.

To finalize the set-up for publishing to PyPi or Artifactory, see
[here](https://jbeirer.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see
[here](https://jbeirer.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://jbeirer.github.io/cookiecutter-poetry/features/codecov/).

## Releasing a new version

- Create an API Token on [Pypi](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting
[this page](https://github.com/jbeirer/pygeosimplify/settings/secrets/actions/new).
- Create a [new release](https://github.com/jbeirer/pygeosimplify/releases/new) on Github.
Create a new tag in the form ``*.*.*``.

For more details, see [here](https://jbeirer.github.io/cookiecutter-poetry/features/cicd/#how-to-trigger-a-release).
