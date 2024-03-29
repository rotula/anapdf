# -*- coding: UTF-8 -*-

"""
Analyze PDF files
"""

__all__ = ["Analyzer", "PDFAnalyzerError",
        "TEIConverter"]
__version__ = "0.4.3"

from .analyzer import Analyzer
from .analyzer import PDFAnalyzerError
from .converters import TEIConverter

