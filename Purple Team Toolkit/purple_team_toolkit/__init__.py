"""
Purple Team Toolkit

A comprehensive cybersecurity toolkit that integrates Red Team attack simulations
with Blue Team defensive monitoring, providing correlation and detailed reporting.
"""

__version__ = "1.0.0"
__author__ = "mooncakesg"
__description__ = "Purple Team cybersecurity toolkit for attack-defense correlation"

from .cli import main
from .purple_logic import PurpleTeamEngine
from .red_team import RedTeamModule
from .blue_team import BlueTeamModule

__all__ = [
    "main",
    "PurpleTeamEngine", 
    "RedTeamModule",
    "BlueTeamModule"
]
