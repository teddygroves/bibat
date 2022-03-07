import os
from shutil import rmtree

REMOVE_PATHS = [
    '{% if cookiecutter.create_writing_directory != "y" %} writing {% endif %}',
    '{% if cookiecutter.create_tests_directory != "y" %} tests {% endif %}',
    '{% if cookiecutter.create_dotgithub_directory != "y" %} .github {% endif %}',
]

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        rmtree(path)
