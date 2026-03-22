"""Filesystem helper utilities."""

import os
from typing import List

SUPPORTED_EXTENSIONS = {".txt", ".csv"}


def list_supported_files(directory: str) -> List[str]:
    """Return absolute paths of supported files inside *directory*.

    Only files whose extension is in ``SUPPORTED_EXTENSIONS`` should be
    returned.
    """
    result: List[str] = []
    for entry in sorted(os.listdir(directory)):
        full = os.path.join(directory, entry)
        if os.path.isfile(full):
            result.append(full)
    return result
