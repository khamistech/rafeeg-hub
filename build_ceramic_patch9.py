#!/usr/bin/env python3
"""Patch 9: حمامات-صغيرة"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ceramic_factory import build_type_patch
build_type_patch("حمامات-صغيرة")
