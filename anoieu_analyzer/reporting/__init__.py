"""Repository reporting helpers used by the human commands in scripts/."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
