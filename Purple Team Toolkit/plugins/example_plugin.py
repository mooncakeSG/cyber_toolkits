"""
Example Plugin for Purple Team Toolkit

This plugin demonstrates how to extend the toolkit with custom functionality.
"""

import logging
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class PluginInfo:
    """Plugin information"""
    name: str = "Example Plugin"
    version: str = "1.0.0"
    description: str = "Example plugin demonstrating extensibility"
    author: str = "Purple Team Toolkit"

class ExamplePlugin:
    """Example plugin class"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.info = PluginInfo()
    
    def get_info(self) -> PluginInfo:
        """Get plugin information"""
        return self.info
    
    def custom_attack_technique(self, target: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Custom attack technique example"""
        self.logger.info(f"Executing custom attack technique on {target}")
        
        # Example custom attack logic
        result = {
            'technique': 'custom_attack',
            'target': target,
            'success': True,
            'data': {
                'custom_parameter': parameters.get('custom_parameter', 'default'),
                'timestamp': '2024-01-01T00:00:00Z'
            },
            'mitre_technique': 'T9999'  # Custom technique
        }
        
        return result
    
    def custom_detection_rule(self, event: Dict[str, Any]) -> bool:
        """Custom detection rule example"""
        # Example custom detection logic
        if 'custom_pattern' in event.get('description', ''):
            return True
        return False
    
    def custom_correlation_logic(self, attack: Dict[str, Any], detection: Dict[str, Any]) -> float:
        """Custom correlation logic example"""
        # Example custom correlation scoring
        confidence = 0.0
        
        # Check for custom indicators
        if attack.get('technique') == 'custom_attack':
            confidence += 0.5
        
        if detection.get('event_type') == 'custom_detection':
            confidence += 0.5
        
        return confidence
    
    def get_custom_payloads(self) -> List[Dict[str, Any]]:
        """Get custom payloads"""
        return [
            {
                'name': 'Custom Payload 1',
                'type': 'custom',
                'content': 'custom_payload_data',
                'description': 'Example custom payload',
                'risk_level': 'LOW'
            },
            {
                'name': 'Custom Payload 2',
                'type': 'custom',
                'content': 'another_custom_payload',
                'description': 'Another example custom payload',
                'risk_level': 'MEDIUM'
            }
        ]

# Plugin registration function
def register_plugin(config: Dict[str, Any]) -> ExamplePlugin:
    """Register the example plugin"""
    return ExamplePlugin(config)
