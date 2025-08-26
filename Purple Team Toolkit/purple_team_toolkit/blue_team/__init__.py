"""
Blue Team Module for Purple Team Toolkit

Provides defensive monitoring and detection capabilities including
log collection, event normalization, and alerting.
"""

from .modules import LogCollector, DetectionEngine, AlertManager
from .normalization import EventNormalizer

# Create a BlueTeamModule class that combines all blue team functionality
class BlueTeamModule:
    """Combined Blue Team module providing all defensive monitoring capabilities."""
    
    def __init__(self):
        self.log_collector = LogCollector()
        self.detection_engine = DetectionEngine()
        self.alert_manager = AlertManager()
        self.event_normalizer = EventNormalizer()

__all__ = [
    "LogCollector",
    "DetectionEngine", 
    "AlertManager",
    "EventNormalizer",
    "BlueTeamModule"
]
