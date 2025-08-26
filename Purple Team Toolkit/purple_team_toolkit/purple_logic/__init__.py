"""
Purple Logic Module for Purple Team Toolkit

Provides correlation between Red Team attacks and Blue Team detections,
coverage analysis, and reporting capabilities.
"""

from .correlation import PurpleTeamEngine, CorrelationResult, CoverageAnalysis

__all__ = [
    "PurpleTeamEngine",
    "CorrelationResult", 
    "CoverageAnalysis"
]
