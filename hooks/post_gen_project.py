import os

REMOVE_PATHS = [
    '{% if cookiecutter.create_writing_dir != "y" %} writing {% endif %}',
]

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        os.rmdir(path)
