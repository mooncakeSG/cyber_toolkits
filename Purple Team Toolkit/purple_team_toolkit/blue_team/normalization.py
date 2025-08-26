"""
Event Normalization for Blue Team Operations

Provides common schema for cross-platform event analysis.
"""

import json
import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class NormalizedEvent:
    """Normalized security event with common schema"""
    event_id: str
    timestamp: float
    source_type: str
    source_name: str
    event_category: str
    event_type: str
    severity: str
    description: str
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    username: Optional[str] = None
    process_name: Optional[str] = None
    file_path: Optional[str] = None
    url: Optional[str] = None
    user_agent: Optional[str] = None
    raw_data: Dict[str, Any] = None
    mitre_technique: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.raw_data is None:
            self.raw_data = {}
        if self.tags is None:
            self.tags = []

class EventNormalizer:
    """Normalizes events from various sources into common schema"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.normalizers: Dict[str, callable] = {}
        self._setup_normalizers()
    
    def _setup_normalizers(self):
        """Setup normalizers for different event sources"""
        self.normalizers = {
            'system': self._normalize_system_event,
            'network': self._normalize_network_event,
            'web_server': self._normalize_web_event,
            'database': self._normalize_database_event,
            'firewall': self._normalize_firewall_event,
            'ids': self._normalize_ids_event,
            'application': self._normalize_application_event
        }
    
    def normalize_event(self, event: Dict[str, Any]) -> NormalizedEvent:
        """Normalize an event based on its source"""
        source_type = event.get('source', 'unknown')
        
        if source_type in self.normalizers:
            return self.normalizers[source_type](event)
        else:
            return self._normalize_generic_event(event)
    
    def normalize_events(self, events: List[Dict[str, Any]]) -> List[NormalizedEvent]:
        """Normalize a list of events"""
        normalized_events = []
        
        for event in events:
            try:
                normalized_event = self.normalize_event(event)
                normalized_events.append(normalized_event)
            except Exception as e:
                self.logger.error(f"Error normalizing event: {e}")
                continue
        
        return normalized_events
    
    def _normalize_system_event(self, event: Dict[str, Any]) -> NormalizedEvent:
        """Normalize system-level events"""
        event_id = event.get('event_id', f"system_{int(time.time())}")
        timestamp = event.get('timestamp', time.time())
        
        # Extract process information
        process_name = None
        if 'raw_data' in event and 'process' in event['raw_data']:
            process_info = event['raw_data']['process']
            process_name = process_info.get('name')
        
        # Extract connection information
        source_ip = None
        destination_ip = None
        source_port = None
        destination_port = None
        
        if 'raw_data' in event and 'connection' in event['raw_data']:
            conn = event['raw_data']['connection']
            if hasattr(conn, 'laddr'):
                source_ip = conn.laddr.ip if conn.laddr else None
                source_port = conn.laddr.port if conn.laddr else None
            if hasattr(conn, 'raddr'):
                destination_ip = conn.raddr.ip if conn.raddr else None
                destination_port = conn.raddr.port if conn.raddr else None
        
        # Determine event category
        event_category = self._determine_event_category(event.get('event_type', ''))
        
        return NormalizedEvent(
            event_id=event_id,
            timestamp=timestamp,
            source_type='system',
            source_name=event.get('source', 'system'),
            event_category=event_category,
            event_type=event.get('event_type', 'unknown'),
            severity=event.get('severity', 'LOW'),
            description=event.get('description', ''),
            source_ip=source_ip,
            destination_ip=destination_ip,
            source_port=source_port,
            destination_port=destination_port,
            process_name=process_name,
            raw_data=event.get('raw_data', {}),
            mitre_technique=event.get('mitre_technique'),
            tags=self._extract_tags(event)
        )
    
    def _normalize_network_event(self, event: Dict[str, Any]) -> NormalizedEvent:
        """Normalize network-level events"""
        event_id = event.get('event_id', f"network_{int(time.time())}")
        timestamp = event.get('timestamp', time.time())
        
        # Extract network information
        source_ip = None
        destination_ip = None
        source_port = None
        destination_port = None
        
        if 'raw_data' in event and 'connection' in event['raw_data']:
            conn = event['raw_data']['connection']
            if hasattr(conn, 'laddr'):
                source_ip = conn.laddr.ip if conn.laddr else None
                source_port = conn.laddr.port if conn.laddr else None
            if hasattr(conn, 'raddr'):
                destination_ip = conn.raddr.ip if conn.raddr else None
                destination_port = conn.raddr.port if conn.raddr else None
        
        # Determine event category
        event_category = self._determine_event_category(event.get('event_type', ''))
        
        return NormalizedEvent(
            event_id=event_id,
            timestamp=timestamp,
            source_type='network',
            source_name=event.get('source', 'network'),
            event_category=event_category,
            event_type=event.get('event_type', 'unknown'),
            severity=event.get('severity', 'LOW'),
            description=event.get('description', ''),
            source_ip=source_ip,
            destination_ip=destination_ip,
            source_port=source_port,
            destination_port=destination_port,
            raw_data=event.get('raw_data', {}),
            mitre_technique=event.get('mitre_technique'),
            tags=self._extract_tags(event)
        )
    
    def _normalize_web_event(self, event: Dict[str, Any]) -> NormalizedEvent:
        """Normalize web server events"""
        event_id = event.get('event_id', f"web_{int(time.time())}")
        timestamp = event.get('timestamp', time.time())
        
        # Extract web-specific information
        source_ip = None
        url = None
        user_agent = None
        
        if 'raw_data' in event:
            raw_data = event['raw_data']
            source_ip = raw_data.get('ip')
            url = raw_data.get('url')
            user_agent = raw_data.get('user_agent')
        
        # Determine event category
        event_category = self._determine_event_category(event.get('event_type', ''))
        
        return NormalizedEvent(
            event_id=event_id,
            timestamp=timestamp,
            source_type='web_server',
            source_name=event.get('source', 'web_server'),
            event_category=event_category,
            event_type=event.get('event_type', 'unknown'),
            severity=event.get('severity', 'LOW'),
            description=event.get('description', ''),
            source_ip=source_ip,
            url=url,
            user_agent=user_agent,
            raw_data=event.get('raw_data', {}),
            mitre_technique=event.get('mitre_technique'),
            tags=self._extract_tags(event)
        )
    
    def _normalize_database_event(self, event: Dict[str, Any]) -> NormalizedEvent:
        """Normalize database events"""
        event_id = event.get('event_id', f"db_{int(time.time())}")
        timestamp = event.get('timestamp', time.time())
        
        # Extract database-specific information
        username = None
        query = None
        
        if 'raw_data' in event:
            raw_data = event['raw_data']
            username = raw_data.get('username')
            query = raw_data.get('query')
        
        # Determine event category
        event_category = self._determine_event_category(event.get('event_type', ''))
        
        return NormalizedEvent(
            event_id=event_id,
            timestamp=timestamp,
            source_type='database',
            source_name=event.get('source', 'database'),
            event_category=event_category,
            event_type=event.get('event_type', 'unknown'),
            severity=event.get('severity', 'LOW'),
            description=event.get('description', ''),
            username=username,
            raw_data=event.get('raw_data', {}),
            mitre_technique=event.get('mitre_technique'),
            tags=self._extract_tags(event)
        )
    
    def _normalize_firewall_event(self, event: Dict[str, Any]) -> NormalizedEvent:
        """Normalize firewall events"""
        event_id = event.get('event_id', f"fw_{int(time.time())}")
        timestamp = event.get('timestamp', time.time())
        
        # Extract firewall-specific information
        source_ip = None
        destination_ip = None
        source_port = None
        destination_port = None
        
        if 'raw_data' in event:
            raw_data = event['raw_data']
            source_ip = raw_data.get('ip')
            destination_ip = raw_data.get('dest_ip')
            source_port = raw_data.get('port')
            destination_port = raw_data.get('dest_port')
        
        # Determine event category
        event_category = self._determine_event_category(event.get('event_type', ''))
        
        return NormalizedEvent(
            event_id=event_id,
            timestamp=timestamp,
            source_type='firewall',
            source_name=event.get('source', 'firewall'),
            event_category=event_category,
            event_type=event.get('event_type', 'unknown'),
            severity=event.get('severity', 'LOW'),
            description=event.get('description', ''),
            source_ip=source_ip,
            destination_ip=destination_ip,
            source_port=source_port,
            destination_port=destination_port,
            raw_data=event.get('raw_data', {}),
            mitre_technique=event.get('mitre_technique'),
            tags=self._extract_tags(event)
        )
    
    def _normalize_ids_event(self, event: Dict[str, Any]) -> NormalizedEvent:
        """Normalize IDS events"""
        event_id = event.get('event_id', f"ids_{int(time.time())}")
        timestamp = event.get('timestamp', time.time())
        
        # Extract IDS-specific information
        source_ip = None
        destination_ip = None
        alert_type = None
        
        if 'raw_data' in event:
            raw_data = event['raw_data']
            source_ip = raw_data.get('source_ip')
            destination_ip = raw_data.get('dest_ip')
            alert_type = raw_data.get('alert_type')
        
        # Determine event category
        event_category = self._determine_event_category(event.get('event_type', ''))
        
        return NormalizedEvent(
            event_id=event_id,
            timestamp=timestamp,
            source_type='ids',
            source_name=event.get('source', 'ids'),
            event_category=event_category,
            event_type=event.get('event_type', 'unknown'),
            severity=event.get('severity', 'LOW'),
            description=event.get('description', ''),
            source_ip=source_ip,
            destination_ip=destination_ip,
            raw_data=event.get('raw_data', {}),
            mitre_technique=event.get('mitre_technique'),
            tags=self._extract_tags(event)
        )
    
    def _normalize_application_event(self, event: Dict[str, Any]) -> NormalizedEvent:
        """Normalize application events"""
        event_id = event.get('event_id', f"app_{int(time.time())}")
        timestamp = event.get('timestamp', time.time())
        
        # Extract application-specific information
        username = None
        file_path = None
        url = None
        
        if 'raw_data' in event:
            raw_data = event['raw_data']
            username = raw_data.get('username')
            file_path = raw_data.get('file_path')
            url = raw_data.get('url')
        
        # Determine event category
        event_category = self._determine_event_category(event.get('event_type', ''))
        
        return NormalizedEvent(
            event_id=event_id,
            timestamp=timestamp,
            source_type='application',
            source_name=event.get('source', 'application'),
            event_category=event_category,
            event_type=event.get('event_type', 'unknown'),
            severity=event.get('severity', 'LOW'),
            description=event.get('description', ''),
            username=username,
            file_path=file_path,
            url=url,
            raw_data=event.get('raw_data', {}),
            mitre_technique=event.get('mitre_technique'),
            tags=self._extract_tags(event)
        )
    
    def _normalize_generic_event(self, event: Dict[str, Any]) -> NormalizedEvent:
        """Normalize generic events"""
        event_id = event.get('event_id', f"generic_{int(time.time())}")
        timestamp = event.get('timestamp', time.time())
        
        # Determine event category
        event_category = self._determine_event_category(event.get('event_type', ''))
        
        return NormalizedEvent(
            event_id=event_id,
            timestamp=timestamp,
            source_type=event.get('source', 'unknown'),
            source_name=event.get('source', 'unknown'),
            event_category=event_category,
            event_type=event.get('event_type', 'unknown'),
            severity=event.get('severity', 'LOW'),
            description=event.get('description', ''),
            raw_data=event.get('raw_data', {}),
            mitre_technique=event.get('mitre_technique'),
            tags=self._extract_tags(event)
        )
    
    def _determine_event_category(self, event_type: str) -> str:
        """Determine the category of an event based on its type"""
        event_type_lower = event_type.lower()
        
        # Authentication events
        if any(keyword in event_type_lower for keyword in ['login', 'auth', 'password', 'credential']):
            return 'authentication'
        
        # Network events
        if any(keyword in event_type_lower for keyword in ['connection', 'port', 'scan', 'network']):
            return 'network'
        
        # File system events
        if any(keyword in event_type_lower for keyword in ['file', 'directory', 'access', 'read', 'write']):
            return 'filesystem'
        
        # Process events
        if any(keyword in event_type_lower for keyword in ['process', 'execution', 'command']):
            return 'process'
        
        # Web events
        if any(keyword in event_type_lower for keyword in ['web', 'http', 'url', 'injection', 'xss']):
            return 'web'
        
        # Database events
        if any(keyword in event_type_lower for keyword in ['sql', 'database', 'query']):
            return 'database'
        
        # System events
        if any(keyword in event_type_lower for keyword in ['system', 'cpu', 'memory', 'resource']):
            return 'system'
        
        return 'unknown'
    
    def _extract_tags(self, event: Dict[str, Any]) -> List[str]:
        """Extract tags from an event"""
        tags = []
        
        # Add source tag
        if 'source' in event:
            tags.append(f"source:{event['source']}")
        
        # Add severity tag
        if 'severity' in event:
            tags.append(f"severity:{event['severity']}")
        
        # Add MITRE technique tag
        if 'mitre_technique' in event:
            tags.append(f"mitre:{event['mitre_technique']}")
        
        # Add event type tag
        if 'event_type' in event:
            tags.append(f"type:{event['event_type']}")
        
        return tags
    
    def get_event_summary(self, events: List[NormalizedEvent]) -> Dict[str, Any]:
        """Generate a summary of normalized events"""
        summary = {
            'total_events': len(events),
            'sources': {},
            'categories': {},
            'severities': {},
            'mitre_techniques': {},
            'time_range': {
                'start': None,
                'end': None
            }
        }
        
        if not events:
            return summary
        
        # Calculate time range
        timestamps = [event.timestamp for event in events]
        summary['time_range']['start'] = min(timestamps)
        summary['time_range']['end'] = max(timestamps)
        
        # Count by various dimensions
        for event in events:
            # Source counts
            source = event.source_type
            summary['sources'][source] = summary['sources'].get(source, 0) + 1
            
            # Category counts
            category = event.event_category
            summary['categories'][category] = summary['categories'].get(category, 0) + 1
            
            # Severity counts
            severity = event.severity
            summary['severities'][severity] = summary['severities'].get(severity, 0) + 1
            
            # MITRE technique counts
            if event.mitre_technique:
                technique = event.mitre_technique
                summary['mitre_techniques'][technique] = summary['mitre_techniques'].get(technique, 0) + 1
        
        return summary
