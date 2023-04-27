Contributing
============

All contributions are very welcome!

Make sure to read the [code of
conduct](https://github.com/teddygroves/bibat/CODE_OF_CONDUCT.md) and follow
its recommendations. 

If you have a specific suggestion for how bibat could be improved, or if you
find a bug then please file an issue or submit a pull request.

Alternatively, if you have any more general thoughts or questions, please post
them in the [discussions page](https://github.com/teddygroves/bibat/discussions).

If you'd like to contribute code changes, just follow the normal github
workflow.

To test changes to the template locally, I recommend avoiding having to complete
the wizard every time by making a [yaml](https://yaml.org/) config file like
this (copied from the file `tests/data/example_config.yml`):

```yaml
default_context:
  project_name: My cool project
  repo_name: my_cool_project
  author_name: Author Name
  author_email: author@email.com
  coc_contact: author@email.com
  description: A short description of the project
  open_source_license: MIT
  docs_format: Markdown
  create_tests_directory: y
  create_dotgithub_directory: y
  install_python_tooling: y
  bibat_version: unknown version
```

You should now be able to create a `my_cool_project` bibat project like this:

```sh
$ bibat --config-file path/to/config.yml
```

To release a new version of bibat, edit the field :`version` in the file
`setup.cfg`, e.g. to `0.2.1` then make a pull request with this change.

Once the changes are merged into the `origin/master` branch, add a tag whose
name begins with `v`, followed by the new version number to your local `master`
branch, for example like this:


```sh
git tag v0.2.1
```

Now push the new tag to github:

```sh
git push origin "v0.2.1"
```
