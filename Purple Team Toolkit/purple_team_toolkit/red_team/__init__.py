"""
Red Team Module for Purple Team Toolkit

Provides attack simulation capabilities including reconnaissance,
exploitation, and post-exploitation activities.
"""

from .modules import ReconnaissanceModule, ExploitationModule, PostExploitationModule
from .payloads import PayloadManager

# Create a RedTeamModule class that combines all red team functionality
class RedTeamModule:
    """Combined Red Team module providing all attack simulation capabilities."""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.reconnaissance = ReconnaissanceModule(self.config)
        self.exploitation = ExploitationModule(self.config)
        self.post_exploitation = PostExploitationModule(self.config)
        self.payload_manager = PayloadManager(self.config)

__all__ = [
    "ReconnaissanceModule",
    "ExploitationModule", 
    "PostExploitationModule",
    "PayloadManager",
    "RedTeamModule"
]
