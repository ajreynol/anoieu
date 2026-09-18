#!/usr/bin/env python3
"""Check repository policy; implementation and contract live in policy_check/."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from policy_check.checker import main

if __name__ == "__main__":
    raise SystemExit(main())
