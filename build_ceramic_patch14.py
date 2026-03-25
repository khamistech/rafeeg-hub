#!/usr/bin/env python3
"""Patch 14: انواع-سيراميك"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ceramic_factory import build_type_patch
build_type_patch("انواع-سيراميك")
