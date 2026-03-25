#!/usr/bin/env python3
"""Patch 4: تركيب-سيراميك-مطابخ (Hub + 4 cities)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from ceramic_factory import build_type_patch
build_type_patch("مطابخ")
