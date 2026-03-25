#!/usr/bin/env python3
"""Patch 8: حدائق"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ceramic_factory import build_type_patch
build_type_patch("حدائق")
