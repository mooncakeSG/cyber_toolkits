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
    
    def __init__(self, config=None):
        self.config = config or {}
        self.log_collector = LogCollector(self.config)
        self.detection_engine = DetectionEngine(self.config)
        self.alert_manager = AlertManager(self.config)
        self.event_normalizer = EventNormalizer(self.config)

__all__ = [
    "LogCollector",
    "DetectionEngine", 
    "AlertManager",
    "EventNormalizer",
    "BlueTeamModule"
]
