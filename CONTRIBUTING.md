# How to contribute to bibat

All contributions are very welcome!

Make sure to read the [code of conduct](https://github.com/teddygroves/bibat/CODE_OF_CONDUCT.md) and follow its recommendations.

If you have a specific suggestion for how bibat could be improved, or if you
find a bug then please file an issue or submit a pull request.

Alternatively, if you have any more general thoughts or questions, please post
them in the [discussions page](https://github.com/teddygroves/bibat/discussions).

If you would like to contribute code changes, just follow the normal [GitHub
workflow](https://docs.github.com/en/get-started/quickstart/github-flow):
make a local branch with the changes then create a pull request.

## Developing bibat locally

To develop bibat locally you will probably need to install it with development
dependencies. Here is how to do so:

```sh
$ pip install bibat'[development]'
```

You can see what these dependencies are by checking the
`[project.optional-dependencies]` table in bibat's [`pyproject.toml` file](https://github.com/teddygroves/bibat/blob/main/pyproject.toml). Some
important ones are [black](https://github.com/psf/black),
[isort](https://pycqa.github.io/isort/),
[pre-commit](https://pre-commit.com/) and [tox](https://tox.wiki/en/latest/).

Another thing you will want to do while developing bibat locally is use it to
create projects. For this I recommend avoiding having to complete the wizard
every time by using copier's `--defaults` (abbreviation `-l`) [option](https://copier.readthedocs.io/en/stable/reference/cli/#copier.cli), e.g.

```sh
$ copier copy -l --vcs-ref HEAD bibat my_cool_project
```

## Cmdstan

Bibat depends on [cmdstan](https://github.com/stan-dev/cmdstan), which can
be tricky to install. If you run the commands `make env` or `make analysis`
from a bibat project, it will attempt to install cmdstan automatically. If
this doesn't work, please check the [cmdstan](https://mc-stan.org/users/interfaces/cmdstan) and [cmdstanpy](https://cmdstanpy.readthedocs.io/en/v1.1.0/installation.html#cmdstan-installation) documentation.

## Releasing new versions of bibat

To release a new version of bibat, edit the field `version` in the file
`pyproject.toml`, e.g. to `0.2.1` then make a pull request with this change.

Once the changes are merged into the `origin/main` branch, add a tag whose name
begins with `v`, followed by the new version number to your local `main` branch,
for example like this:

```sh
$ git tag v0.2.1
```

Now push the new tag to GitHub:

```sh
$ git push origin "v0.2.1"
```
