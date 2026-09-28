#!/usr/bin/env python

import sys
import traceback

from .indexer import synchronize


if __name__ == '__main__':
    try:
        synchronize(rebuild=True)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
