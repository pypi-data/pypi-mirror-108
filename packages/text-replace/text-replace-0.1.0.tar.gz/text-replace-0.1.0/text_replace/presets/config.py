"""Sets up the environment by adding the root directory to `sys.path`."""

import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
)
