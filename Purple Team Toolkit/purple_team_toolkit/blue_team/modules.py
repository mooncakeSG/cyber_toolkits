"""
Blue Team Monitoring and Detection Modules

Provides defensive capabilities including log collection, detection,
and alerting for Purple Team testing.
"""

import json
import time
import logging
import re
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from pathlib import Path
import threading
from datetime import datetime
import psutil
import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

@dataclass
class SecurityEvent:
    """Represents a security event"""
    timestamp: float
    source: str
    event_type: str
    severity: str
    description: str
    raw_data: Dict[str, Any]
    normalized_data: Dict[str, Any] = None
    mitre_technique: Optional[str] = None
    event_id: Optional[str] = None

@dataclass
class DetectionRule:
    """Represents a detection rule"""
    name: str
    description: str
    pattern: str
    severity: str
    mitre_technique: Optional[str] = None
    enabled: bool = True
    action: str = "alert"

class LogCollector:
    """Collects logs from various sources"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.collectors: Dict[str, Callable] = {}
        self.events: List[SecurityEvent] = []
        self._setup_collectors()
    
    def _setup_collectors(self):
        """Setup various log collectors"""
        self.collectors = {
            'system_logs': self._collect_system_logs,
            'network_logs': self._collect_network_logs,
            'application_logs': self._collect_application_logs,
            'security_logs': self._collect_security_logs
        }
    
    def collect_logs(self, source: str) -> List[SecurityEvent]:
        """Collect logs from specified source"""
        if source in self.collectors:
            return self.collectors[source]()
        else:
            self.logger.warning(f"Unknown log source: {source}")
            return []
    
    def _collect_system_logs(self) -> List[SecurityEvent]:
        """Collect system-level logs"""
        events = []
        
        try:
            # Collect process information
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'connections']):
                try:
                    proc_info = proc.info
                    
                    # Look for suspicious processes
                    if self._is_suspicious_process(proc_info):
                        event = SecurityEvent(
                            timestamp=time.time(),
                            source="system",
                            event_type="suspicious_process",
                            severity="MEDIUM",
                            description=f"Suspicious process detected: {proc_info['name']}",
                            raw_data=proc_info,
                            mitre_technique="T1055"
                        )
                        events.append(event)
                    
                    # Check for network connections
                    if proc_info['connections']:
                        for conn in proc_info['connections']:
                            if self._is_suspicious_connection(conn):
                                event = SecurityEvent(
                                    timestamp=time.time(),
                                    source="system",
                                    event_type="suspicious_connection",
                                    severity="HIGH",
                                    description=f"Suspicious connection from {proc_info['name']}",
                                    raw_data={'process': proc_info, 'connection': conn},
                                    mitre_technique="T1071"
                                )
                                events.append(event)
                                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Collect system resource usage
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            if cpu_percent > 80:
                event = SecurityEvent(
                    timestamp=time.time(),
                    source="system",
                    event_type="high_cpu_usage",
                    severity="LOW",
                    description=f"High CPU usage detected: {cpu_percent}%",
                    raw_data={'cpu_percent': cpu_percent},
                    mitre_technique="T1499"
                )
                events.append(event)
            
            if memory.percent > 90:
                event = SecurityEvent(
                    timestamp=time.time(),
                    source="system",
                    event_type="high_memory_usage",
                    severity="LOW",
                    description=f"High memory usage detected: {memory.percent}%",
                    raw_data={'memory_percent': memory.percent},
                    mitre_technique="T1499"
                )
                events.append(event)
                
        except Exception as e:
            self.logger.error(f"Error collecting system logs: {e}")
        
        return events
    
    def _collect_network_logs(self) -> List[SecurityEvent]:
        """Collect network-related logs"""
        events = []
        
        try:
            # Collect network connections
            connections = psutil.net_connections()
            
            for conn in connections:
                if conn.status == 'ESTABLISHED':
                    # Check for suspicious connections
                    if self._is_suspicious_connection(conn):
                        event = SecurityEvent(
                            timestamp=time.time(),
                            source="network",
                            event_type="suspicious_connection",
                            severity="HIGH",
                            description=f"Suspicious network connection detected",
                            raw_data={'connection': conn._asdict()},
                            mitre_technique="T1071"
                        )
                        events.append(event)
                    
                    # Check for connections to known malicious IPs
                    if self._is_malicious_ip(conn.raddr.ip if conn.raddr else None):
                        event = SecurityEvent(
                            timestamp=time.time(),
                            source="network",
                            event_type="malicious_connection",
                            severity="CRITICAL",
                            description=f"Connection to known malicious IP: {conn.raddr.ip}",
                            raw_data={'connection': conn._asdict()},
                            mitre_technique="T1071"
                        )
                        events.append(event)
            
            # Collect network statistics
            net_io = psutil.net_io_counters()
            
            # Check for unusual network activity
            if net_io.bytes_sent > 1000000000:  # 1GB
                event = SecurityEvent(
                    timestamp=time.time(),
                    source="network",
                    event_type="high_network_activity",
                    severity="MEDIUM",
                    description=f"High network activity detected: {net_io.bytes_sent} bytes sent",
                    raw_data={'network_io': net_io._asdict()},
                    mitre_technique="T1041"
                )
                events.append(event)
                
        except Exception as e:
            self.logger.error(f"Error collecting network logs: {e}")
        
        return events
    
    def _collect_application_logs(self) -> List[SecurityEvent]:
        """Collect application-specific logs"""
        events = []
        
        # This would normally read from actual log files
        # For simulation, we'll create some sample events
        
        sample_events = [
            {
                'timestamp': time.time(),
                'source': 'web_server',
                'event_type': 'failed_login',
                'severity': 'MEDIUM',
                'description': 'Multiple failed login attempts detected',
                'raw_data': {'ip': '192.168.1.100', 'attempts': 5},
                'mitre_technique': 'T1110'
            },
            {
                'timestamp': time.time(),
                'source': 'database',
                'event_type': 'sql_injection_attempt',
                'severity': 'HIGH',
                'description': 'SQL injection attempt detected',
                'raw_data': {'query': "SELECT * FROM users WHERE id='1' OR '1'='1'"},
                'mitre_technique': 'T1190'
            }
        ]
        
        for event_data in sample_events:
            event = SecurityEvent(**event_data)
            events.append(event)
        
        return events
    
    def _collect_security_logs(self) -> List[SecurityEvent]:
        """Collect security-specific logs"""
        events = []
        
        # Simulate security events
        security_events = [
            {
                'timestamp': time.time(),
                'source': 'firewall',
                'event_type': 'blocked_connection',
                'severity': 'MEDIUM',
                'description': 'Firewall blocked suspicious connection',
                'raw_data': {'ip': '10.0.0.100', 'port': 22, 'reason': 'brute_force'},
                'mitre_technique': 'T1021'
            },
            {
                'timestamp': time.time(),
                'source': 'ids',
                'event_type': 'intrusion_detected',
                'severity': 'HIGH',
                'description': 'Intrusion detection system alert',
                'raw_data': {'alert_type': 'port_scan', 'source_ip': '192.168.1.50'},
                'mitre_technique': 'T1046'
            }
        ]
        
        for event_data in security_events:
            event = SecurityEvent(**event_data)
            events.append(event)
        
        return events
    
    def _is_suspicious_process(self, proc_info: Dict[str, Any]) -> bool:
        """Check if a process is suspicious"""
        suspicious_names = [
            'nc', 'netcat', 'ncat', 'telnet', 'rsh', 'rlogin',
            'wget', 'curl', 'powershell', 'cmd', 'bash'
        ]
        
        return proc_info['name'] in suspicious_names
    
    def _is_suspicious_connection(self, conn) -> bool:
        """Check if a connection is suspicious"""
        # Check for connections to suspicious ports
        suspicious_ports = [22, 23, 3389, 5900, 8080]
        
        if hasattr(conn, 'raddr') and conn.raddr:
            return conn.raddr.port in suspicious_ports
        
        return False
    
    def _is_malicious_ip(self, ip: Optional[str]) -> bool:
        """Check if an IP is known to be malicious"""
        if not ip:
            return False
        
        # This would normally check against threat intelligence feeds
        # For simulation, we'll use a simple list
        malicious_ips = [
            '192.168.1.100',
            '10.0.0.50',
            '172.16.0.25'
        ]
        
        return ip in malicious_ips

class DetectionEngine:
    """Detects security events based on rules"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.rules: List[DetectionRule] = []
        self._load_default_rules()
    
    def _load_default_rules(self):
        """Load default detection rules"""
        default_rules = [
            DetectionRule(
                name="Port Scan Detection",
                description="Detect port scanning activity",
                pattern=r"port.*scan|nmap|masscan",
                severity="MEDIUM",
                mitre_technique="T1046"
            ),
            DetectionRule(
                name="SQL Injection Detection",
                description="Detect SQL injection attempts",
                pattern=r"(\b(union|select|insert|update|delete|drop|create|alter)\b.*\b(union|select|insert|update|delete|drop|create|alter)\b)|(\b(or|and)\b.*\b(1=1|1=0)\b)",
                severity="HIGH",
                mitre_technique="T1190"
            ),
            DetectionRule(
                name="XSS Detection",
                description="Detect cross-site scripting attempts",
                pattern=r"<script.*?>|<iframe.*?>|javascript:|vbscript:|onload=|onerror=",
                severity="HIGH",
                mitre_technique="T1189"
            ),
            DetectionRule(
                name="Brute Force Detection",
                description="Detect brute force attacks",
                pattern=r"failed.*login|authentication.*failed|invalid.*credentials",
                severity="MEDIUM",
                mitre_technique="T1110"
            ),
            DetectionRule(
                name="File Upload Detection",
                description="Detect suspicious file uploads",
                pattern=r"\.(php|jsp|asp|aspx|exe|bat|cmd|ps1|sh)$",
                severity="HIGH",
                mitre_technique="T1105"
            ),
            DetectionRule(
                name="Command Injection Detection",
                description="Detect command injection attempts",
                pattern=r"[;&|`]|(\b(cat|ls|dir|whoami|id|pwd|wget|curl|nc|netcat)\b)",
                severity="HIGH",
                mitre_technique="T1190"
            )
        ]
        
        self.rules.extend(default_rules)
    
    def add_rule(self, rule: DetectionRule):
        """Add a new detection rule"""
        self.rules.append(rule)
        self.logger.info(f"Added detection rule: {rule.name}")
    
    def remove_rule(self, rule_name: str) -> bool:
        """Remove a detection rule by name"""
        for i, rule in enumerate(self.rules):
            if rule.name == rule_name:
                del self.rules[i]
                self.logger.info(f"Removed detection rule: {rule_name}")
                return True
        return False
    
    def detect_events(self, events: List[SecurityEvent]) -> List[SecurityEvent]:
        """Apply detection rules to events"""
        detected_events = []
        
        for event in events:
            for rule in self.rules:
                if not rule.enabled:
                    continue
                
                # Check if event matches rule pattern
                if self._matches_rule(event, rule):
                    detected_event = SecurityEvent(
                        timestamp=event.timestamp,
                        source=event.source,
                        event_type=f"detected_{event.event_type}",
                        severity=rule.severity,
                        description=f"Detection Rule '{rule.name}': {event.description}",
                        raw_data=event.raw_data,
                        normalized_data=event.normalized_data,
                        mitre_technique=rule.mitre_technique,
                        event_id=f"{rule.name}_{int(event.timestamp)}"
                    )
                    detected_events.append(detected_event)
        
        return detected_events
    
    def _matches_rule(self, event: SecurityEvent, rule: DetectionRule) -> bool:
        """Check if an event matches a detection rule"""
        # Check description
        if re.search(rule.pattern, event.description, re.IGNORECASE):
            return True
        
        # Check raw data
        raw_data_str = json.dumps(event.raw_data)
        if re.search(rule.pattern, raw_data_str, re.IGNORECASE):
            return True
        
        # Check normalized data
        if event.normalized_data:
            normalized_data_str = json.dumps(event.normalized_data)
            if re.search(rule.pattern, normalized_data_str, re.IGNORECASE):
                return True
        
        return False
    
    def get_rules(self) -> List[Dict[str, Any]]:
        """Get all detection rules"""
        return [
            {
                'name': rule.name,
                'description': rule.description,
                'pattern': rule.pattern,
                'severity': rule.severity,
                'mitre_technique': rule.mitre_technique,
                'enabled': rule.enabled,
                'action': rule.action
            }
            for rule in self.rules
        ]

class AlertManager:
    """Manages security alerts and notifications"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.alerts: List[SecurityEvent] = []
        self.alert_handlers: Dict[str, Callable] = {}
        self._setup_alert_handlers()
    
    def _setup_alert_handlers(self):
        """Setup alert handlers"""
        self.alert_handlers = {
            'log': self._log_alert,
            'console': self._console_alert,
            'file': self._file_alert
        }
    
    def create_alert(self, event: SecurityEvent) -> SecurityEvent:
        """Create an alert from a security event"""
        alert = SecurityEvent(
            timestamp=event.timestamp,
            source=event.source,
            event_type=f"alert_{event.event_type}",
            severity=event.severity,
            description=f"ALERT: {event.description}",
            raw_data=event.raw_data,
            normalized_data=event.normalized_data,
            mitre_technique=event.mitre_technique,
            event_id=f"alert_{int(event.timestamp)}_{hash(event.description)}"
        )
        
        self.alerts.append(alert)
        self.logger.info(f"Created alert: {alert.description}")
        
        return alert
    
    def process_alerts(self, events: List[SecurityEvent]) -> List[SecurityEvent]:
        """Process events and create alerts for high-severity events"""
        alerts = []
        
        for event in events:
            # Create alerts for high and critical severity events
            if event.severity in ['HIGH', 'CRITICAL']:
                alert = self.create_alert(event)
                alerts.append(alert)
        
        return alerts
    
    def send_alert(self, alert: SecurityEvent, handler: str = 'console'):
        """Send an alert using specified handler"""
        if handler in self.alert_handlers:
            self.alert_handlers[handler](alert)
        else:
            self.logger.warning(f"Unknown alert handler: {handler}")
    
    def _log_alert(self, alert: SecurityEvent):
        """Log alert to file"""
        alert_data = {
            'timestamp': datetime.fromtimestamp(alert.timestamp).isoformat(),
            'severity': alert.severity,
            'source': alert.source,
            'description': alert.description,
            'mitre_technique': alert.mitre_technique
        }
        
        self.logger.warning(f"SECURITY ALERT: {json.dumps(alert_data)}")
    
    def _console_alert(self, alert: SecurityEvent):
        """Display alert in console"""
        print(f"\n[!] SECURITY ALERT [{alert.severity}]")
        print(f"    Source: {alert.source}")
        print(f"    Description: {alert.description}")
        print(f"    MITRE Technique: {alert.mitre_technique}")
        print(f"    Time: {datetime.fromtimestamp(alert.timestamp).isoformat()}")
        print()
    
    def _file_alert(self, alert: SecurityEvent):
        """Write alert to file"""
        alert_file = Path(self.config.get('alert_file', 'alerts.log'))
        alert_file.parent.mkdir(parents=True, exist_ok=True)
        
        alert_data = {
            'timestamp': datetime.fromtimestamp(alert.timestamp).isoformat(),
            'severity': alert.severity,
            'source': alert.source,
            'description': alert.description,
            'mitre_technique': alert.mitre_technique,
            'raw_data': alert.raw_data
        }
        
        with open(alert_file, 'a') as f:
            f.write(json.dumps(alert_data) + '\n')
    
    def get_alerts(self, severity: Optional[str] = None) -> List[SecurityEvent]:
        """Get alerts, optionally filtered by severity"""
        if severity:
            return [alert for alert in self.alerts if alert.severity == severity]
        return self.alerts
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts.clear()
        self.logger.info("Cleared all alerts")
