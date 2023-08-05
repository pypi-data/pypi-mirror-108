# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""
Confidential ML utilities.
"""


from .constants import DataCategory  # noqa: F401
from .logging import enable_confidential_logging  # noqa: F401
from .exceptions import prefix_stack_trace  # noqa: F401
import warnings

__version__ = "0.9.1"
warnings.warn(
    "This package has been deprecated as of May 2021. "
    "Please install `pip install shrike` and use `shrike.compliant_logging` instead. "
    "More details: https://github.com/Azure/shrike"
)
