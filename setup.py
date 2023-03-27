"""Do the setup.

Before running the function `setup`, this script checks the current Python
version and fails if it is not supported. The `python_requires` field in the
file `setup.cfg` should do this job for new versions of pip; the code here is
to cover other cases.

"""

import sys

from setuptools import setup

MIN_PYTHON = (3, 9)
assert (
    sys.version_info >= MIN_PYTHON
), f"Bibat requires Python {'.'.join([str(n) for n in MIN_PYTHON])} or newer!"

setup()
