import os
from shutil import rmtree

SPHINX_ONLY_PATHS = [
    os.path.join("docs", f)
    for f in (
        "_build",
        "_static",
        "_templates",
        "conf.py",
        "index.rst",
        "make.bat",
    )
]
MARKDOWN_ONLY_PATHS = [
    os.path.join("docs", f) for f in ("report.md", "bibliography.bib")
]

REMOVE_PATHS = [
#    '{% if cookiecutter.install_python_tooling != "y" %} requirements-tooling.txt {% endif %}',
    '{% if cookiecutter.docs_format == "No docs" %} docs {% endif %}',
    '{% if cookiecutter.create_tests_directory != "y" %} tests {% endif %}',
    '{% if cookiecutter.create_dotgithub_directory != "y" %} .github {% endif %}',
]
if "{{ cookiecutter.docs_format }}" not in ["Sphinx", "No docs"]:
    REMOVE_PATHS += SPHINX_ONLY_PATHS

if "{{ cookiecutter.docs_format }}" not in ["Markdown", "No docs"]:
    REMOVE_PATHS += MARKDOWN_ONLY_PATHS

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
