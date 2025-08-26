"""
Payload Management for Red Team Operations

Provides safe, sandboxed payloads for testing various attack vectors.
"""

import json
import base64
import hashlib
import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import random
import string

@dataclass
class Payload:
    """Represents a test payload"""
    name: str
    type: str
    content: str
    description: str
    mitre_technique: Optional[str] = None
    risk_level: str = "LOW"
    sandbox_safe: bool = True
    hash: Optional[str] = None
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()
        if self.hash is None:
            self.hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """Calculate SHA256 hash of payload content"""
        return hashlib.sha256(self.content.encode()).hexdigest()

class PayloadManager:
    """Manages payloads for Red Team operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.payloads: Dict[str, Payload] = {}
        self._load_default_payloads()
    
    def _load_default_payloads(self):
        """Load default test payloads"""
        default_payloads = [
            # Web payloads
            Payload(
                name="SQL Injection Test",
                type="web",
                content="' OR 1=1--",
                description="Basic SQL injection test payload",
                mitre_technique="T1190",
                risk_level="MEDIUM"
            ),
            Payload(
                name="XSS Test",
                type="web", 
                content="<script>alert('XSS Test')</script>",
                description="Basic XSS test payload",
                mitre_technique="T1189",
                risk_level="LOW"
            ),
            Payload(
                name="Command Injection Test",
                type="web",
                content="; ls -la",
                description="Basic command injection test",
                mitre_technique="T1190",
                risk_level="MEDIUM"
            ),
            
            # Network payloads
            Payload(
                name="Port Scan Payload",
                type="network",
                content="nmap -sS -p 80,443,22,21",
                description="Basic port scan command",
                mitre_technique="T1046",
                risk_level="LOW"
            ),
            Payload(
                name="DNS Query Payload",
                type="network",
                content="nslookup example.com",
                description="DNS query test",
                mitre_technique="T1590",
                risk_level="LOW"
            ),
            
            # File system payloads
            Payload(
                name="File Read Test",
                type="filesystem",
                content="/etc/passwd",
                description="Attempt to read system file",
                mitre_technique="T1005",
                risk_level="LOW"
            ),
            Payload(
                name="Directory Traversal Test",
                type="filesystem",
                content="../../../etc/passwd",
                description="Directory traversal test",
                mitre_technique="T1190",
                risk_level="MEDIUM"
            ),
            
            # Authentication payloads
            Payload(
                name="Weak Password Test",
                type="auth",
                content="admin:admin",
                description="Common weak credentials",
                mitre_technique="T1078",
                risk_level="LOW"
            ),
            Payload(
                name="Brute Force Test",
                type="auth",
                content="admin:password123",
                description="Common password test",
                mitre_technique="T1110",
                risk_level="MEDIUM"
            )
        ]
        
        for payload in default_payloads:
            self.payloads[payload.name] = payload
    
    def get_payload(self, name: str) -> Optional[Payload]:
        """Get a payload by name"""
        return self.payloads.get(name)
    
    def get_payloads_by_type(self, payload_type: str) -> List[Payload]:
        """Get all payloads of a specific type"""
        return [p for p in self.payloads.values() if p.type == payload_type]
    
    def get_safe_payloads(self) -> List[Payload]:
        """Get all sandbox-safe payloads"""
        return [p for p in self.payloads.values() if p.sandbox_safe]
    
    def add_payload(self, payload: Payload):
        """Add a new payload"""
        self.payloads[payload.name] = payload
        self.logger.info(f"Added payload: {payload.name}")
    
    def remove_payload(self, name: str) -> bool:
        """Remove a payload by name"""
        if name in self.payloads:
            del self.payloads[name]
            self.logger.info(f"Removed payload: {name}")
            return True
        return False
    
    def list_payloads(self) -> List[Dict[str, Any]]:
        """List all available payloads"""
        return [
            {
                'name': p.name,
                'type': p.type,
                'description': p.description,
                'risk_level': p.risk_level,
                'sandbox_safe': p.sandbox_safe,
                'mitre_technique': p.mitre_technique
            }
            for p in self.payloads.values()
        ]
    
    def generate_custom_payload(self, payload_type: str, **kwargs) -> Payload:
        """Generate a custom payload based on type and parameters"""
        
        if payload_type == "web":
            return self._generate_web_payload(**kwargs)
        elif payload_type == "network":
            return self._generate_network_payload(**kwargs)
        elif payload_type == "filesystem":
            return self._generate_filesystem_payload(**kwargs)
        elif payload_type == "auth":
            return self._generate_auth_payload(**kwargs)
        else:
            raise ValueError(f"Unknown payload type: {payload_type}")
    
    def _generate_web_payload(self, **kwargs) -> Payload:
        """Generate web-based payload"""
        attack_type = kwargs.get('attack_type', 'xss')
        target = kwargs.get('target', 'test')
        
        if attack_type == 'xss':
            content = f"<script>alert('{target}')</script>"
            description = f"XSS payload targeting {target}"
            mitre_technique = "T1189"
        elif attack_type == 'sqli':
            content = f"' UNION SELECT 1,2,3--"
            description = f"SQL injection payload"
            mitre_technique = "T1190"
        elif attack_type == 'lfi':
            content = f"../../../etc/passwd"
            description = f"Local file inclusion payload"
            mitre_technique = "T1190"
        else:
            content = f"<!-- {target} test payload -->"
            description = f"Generic web payload for {target}"
            mitre_technique = "T1190"
        
        return Payload(
            name=f"Custom Web {attack_type.upper()}",
            type="web",
            content=content,
            description=description,
            mitre_technique=mitre_technique,
            risk_level="LOW"
        )
    
    def _generate_network_payload(self, **kwargs) -> Payload:
        """Generate network-based payload"""
        scan_type = kwargs.get('scan_type', 'port')
        target = kwargs.get('target', 'localhost')
        
        if scan_type == 'port':
            ports = kwargs.get('ports', '80,443,22')
            content = f"nmap -sS -p {ports} {target}"
            description = f"Port scan of {target}"
            mitre_technique = "T1046"
        elif scan_type == 'dns':
            content = f"nslookup {target}"
            description = f"DNS query for {target}"
            mitre_technique = "T1590"
        else:
            content = f"ping -c 1 {target}"
            description = f"Ping test for {target}"
            mitre_technique = "T1046"
        
        return Payload(
            name=f"Custom Network {scan_type.upper()}",
            type="network",
            content=content,
            description=description,
            mitre_technique=mitre_technique,
            risk_level="LOW"
        )
    
    def _generate_filesystem_payload(self, **kwargs) -> Payload:
        """Generate filesystem-based payload"""
        operation = kwargs.get('operation', 'read')
        path = kwargs.get('path', '/etc/passwd')
        
        if operation == 'read':
            content = f"cat {path}"
            description = f"File read operation: {path}"
            mitre_technique = "T1005"
        elif operation == 'list':
            content = f"ls -la {path}"
            description = f"Directory listing: {path}"
            mitre_technique = "T1083"
        else:
            content = f"stat {path}"
            description = f"File stat operation: {path}"
            mitre_technique = "T1005"
        
        return Payload(
            name=f"Custom Filesystem {operation.upper()}",
            type="filesystem",
            content=content,
            description=description,
            mitre_technique=mitre_technique,
            risk_level="LOW"
        )
    
    def _generate_auth_payload(self, **kwargs) -> Payload:
        """Generate authentication-based payload"""
        auth_type = kwargs.get('auth_type', 'password')
        username = kwargs.get('username', 'admin')
        
        if auth_type == 'password':
            password = kwargs.get('password', 'password123')
            content = f"{username}:{password}"
            description = f"Password test for {username}"
            mitre_technique = "T1110"
        elif auth_type == 'token':
            content = f"Bearer {self._generate_random_token()}"
            description = f"Token-based auth test"
            mitre_technique = "T1078"
        else:
            content = f"{username}:"
            description = f"Username test: {username}"
            mitre_technique = "T1078"
        
        return Payload(
            name=f"Custom Auth {auth_type.upper()}",
            type="auth",
            content=content,
            description=description,
            mitre_technique=mitre_technique,
            risk_level="LOW"
        )
    
    def _generate_random_token(self, length: int = 32) -> str:
        """Generate a random token for testing"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def save_payloads(self, filepath: str):
        """Save payloads to file"""
        payloads_data = []
        for payload in self.payloads.values():
            payloads_data.append({
                'name': payload.name,
                'type': payload.type,
                'content': payload.content,
                'description': payload.description,
                'mitre_technique': payload.mitre_technique,
                'risk_level': payload.risk_level,
                'sandbox_safe': payload.sandbox_safe,
                'hash': payload.hash,
                'created_at': payload.created_at
            })
        
        with open(filepath, 'w') as f:
            json.dump(payloads_data, f, indent=2)
        
        self.logger.info(f"Saved {len(payloads_data)} payloads to {filepath}")
    
    def load_payloads(self, filepath: str):
        """Load payloads from file"""
        with open(filepath, 'r') as f:
            payloads_data = json.load(f)
        
        for payload_data in payloads_data:
            payload = Payload(
                name=payload_data['name'],
                type=payload_data['type'],
                content=payload_data['content'],
                description=payload_data['description'],
                mitre_technique=payload_data.get('mitre_technique'),
                risk_level=payload_data.get('risk_level', 'LOW'),
                sandbox_safe=payload_data.get('sandbox_safe', True),
                hash=payload_data.get('hash'),
                created_at=payload_data.get('created_at')
            )
            self.payloads[payload.name] = payload
        
        self.logger.info(f"Loaded {len(payloads_data)} payloads from {filepath}")
