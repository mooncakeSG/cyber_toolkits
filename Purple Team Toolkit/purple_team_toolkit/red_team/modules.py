"""
Red Team Attack Modules

Provides various attack simulation capabilities for Purple Team testing.
"""

import nmap
import dns.resolver
import whois
import requests
import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import subprocess
import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class AttackResult:
    """Result of an attack execution"""
    technique: str
    target: str
    success: bool
    data: Dict[str, Any]
    timestamp: float
    mitre_technique: Optional[str] = None
    description: str = ""

class ReconnaissanceModule:
    """Network and target reconnaissance capabilities"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        try:
            self.nm = nmap.PortScanner()
            self.nmap_available = True
        except Exception as e:
            self.logger.warning(f"Nmap not available: {e}")
            self.nm = None
            self.nmap_available = False
    
    def nmap_scan(self, target: str, scan_type: str = "basic") -> AttackResult:
        """Perform network scanning using nmap"""
        if not self.nmap_available:
            return AttackResult(
                technique="nmap_scan",
                target=target,
                success=False,
                data={'error': 'Nmap not available'},
                timestamp=time.time(),
                mitre_technique="T1046",
                description="Nmap scan failed: nmap not available"
            )
        
        try:
            self.logger.info(f"Starting nmap scan of {target}")
            
            if scan_type == "basic":
                scan_args = "-sS -sV -O --top-ports 100"
            elif scan_type == "full":
                scan_args = "-sS -sV -O -A -p-"
            elif scan_type == "stealth":
                scan_args = "-sS -sV --top-ports 20 --timing 2"
            else:
                scan_args = scan_type
            
            self.nm.scan(hosts=target, arguments=scan_args)
            
            results = {
                'hosts': {},
                'scan_stats': self.nm.scanstats()
            }
            
            for host in self.nm.all_hosts():
                results['hosts'][host] = {
                    'state': self.nm[host].state(),
                    'ports': {}
                }
                
                for proto in self.nm[host].all_protocols():
                    ports = self.nm[host][proto].keys()
                    for port in ports:
                        results['hosts'][host]['ports'][port] = {
                            'state': self.nm[host][proto][port]['state'],
                            'service': self.nm[host][proto][port]['name'],
                            'version': self.nm[host][proto][port].get('version', ''),
                            'product': self.nm[host][proto][port].get('product', '')
                        }
            
            return AttackResult(
                technique="nmap_scan",
                target=target,
                success=True,
                data=results,
                timestamp=time.time(),
                mitre_technique="T1046",
                description=f"Nmap {scan_type} scan completed"
            )
            
        except Exception as e:
            self.logger.error(f"Nmap scan failed: {e}")
            return AttackResult(
                technique="nmap_scan",
                target=target,
                success=False,
                data={'error': str(e)},
                timestamp=time.time(),
                mitre_technique="T1046",
                description=f"Nmap scan failed: {e}"
            )
    
    def dns_enumeration(self, domain: str) -> AttackResult:
        """Perform DNS enumeration"""
        try:
            self.logger.info(f"Starting DNS enumeration of {domain}")
            
            results = {
                'a_records': [],
                'aaaa_records': [],
                'mx_records': [],
                'ns_records': [],
                'txt_records': [],
                'subdomains': []
            }
            
            # Common record types
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    for answer in answers:
                        results[f'{record_type.lower()}_records'].append(str(answer))
                except Exception as e:
                    self.logger.debug(f"Failed to resolve {record_type} records: {e}")
            
            # Subdomain enumeration
            common_subdomains = [
                'www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'test',
                'api', 'cdn', 'static', 'img', 'images', 'support'
            ]
            
            for subdomain in common_subdomains:
                try:
                    full_domain = f"{subdomain}.{domain}"
                    answers = dns.resolver.resolve(full_domain, 'A')
                    results['subdomains'].append({
                        'subdomain': subdomain,
                        'ip': str(answers[0])
                    })
                except Exception:
                    pass
            
            return AttackResult(
                technique="dns_enumeration",
                target=domain,
                success=True,
                data=results,
                timestamp=time.time(),
                mitre_technique="T1590",
                description="DNS enumeration completed"
            )
            
        except Exception as e:
            self.logger.error(f"DNS enumeration failed: {e}")
            return AttackResult(
                technique="dns_enumeration",
                target=domain,
                success=False,
                data={'error': str(e)},
                timestamp=time.time(),
                mitre_technique="T1590",
                description=f"DNS enumeration failed: {e}"
            )
    
    def whois_lookup(self, target: str) -> AttackResult:
        """Perform WHOIS lookup"""
        try:
            self.logger.info(f"Starting WHOIS lookup for {target}")
            
            # Try different ways to call whois
            try:
                w = whois.whois(target)
            except AttributeError:
                # Fallback for different whois package versions
                w = whois.query(target)
            
            results = {
                'domain_name': w.domain_name,
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'updated_date': str(w.updated_date),
                'name_servers': w.name_servers,
                'status': w.status,
                'emails': w.emails
            }
            
            return AttackResult(
                technique="whois_lookup",
                target=target,
                success=True,
                data=results,
                timestamp=time.time(),
                mitre_technique="T1590",
                description="WHOIS lookup completed"
            )
            
        except Exception as e:
            self.logger.error(f"WHOIS lookup failed: {e}")
            return AttackResult(
                technique="whois_lookup",
                target=target,
                success=False,
                data={'error': str(e)},
                timestamp=time.time(),
                mitre_technique="T1590",
                description=f"WHOIS lookup failed: {e}"
            )

class ExploitationModule:
    """Exploitation testing capabilities"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def web_fuzzing(self, target: str, wordlist: Optional[List[str]] = None) -> AttackResult:
        """Perform web application fuzzing"""
        try:
            self.logger.info(f"Starting web fuzzing of {target}")
            
            if not wordlist:
                wordlist = [
                    'admin', 'login', 'wp-admin', 'phpmyadmin', 'config',
                    'backup', 'test', 'dev', 'api', 'v1', 'v2', 'docs'
                ]
            
            results = {
                'found_paths': [],
                'status_codes': {},
                'errors': []
            }
            
            for path in wordlist:
                try:
                    url = f"{target.rstrip('/')}/{path}"
                    response = requests.get(url, timeout=10, allow_redirects=False)
                    
                    if response.status_code != 404:
                        results['found_paths'].append({
                            'path': path,
                            'url': url,
                            'status_code': response.status_code,
                            'content_length': len(response.content)
                        })
                        
                        if response.status_code not in results['status_codes']:
                            results['status_codes'][response.status_code] = 0
                        results['status_codes'][response.status_code] += 1
                        
                except Exception as e:
                    results['errors'].append(f"Error testing {path}: {e}")
            
            return AttackResult(
                technique="web_fuzzing",
                target=target,
                success=True,
                data=results,
                timestamp=time.time(),
                mitre_technique="T1590",
                description="Web fuzzing completed"
            )
            
        except Exception as e:
            self.logger.error(f"Web fuzzing failed: {e}")
            return AttackResult(
                technique="web_fuzzing",
                target=target,
                success=False,
                data={'error': str(e)},
                timestamp=time.time(),
                mitre_technique="T1590",
                description=f"Web fuzzing failed: {e}"
            )
    
    def port_scan(self, target: str, ports: Optional[List[int]] = None) -> AttackResult:
        """Perform port scanning"""
        try:
            self.logger.info(f"Starting port scan of {target}")
            
            if not ports:
                ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
            
            results = {
                'open_ports': [],
                'closed_ports': [],
                'filtered_ports': []
            }
            
            def scan_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex((target, port))
                    sock.close()
                    
                    if result == 0:
                        return port, 'open'
                    else:
                        return port, 'closed'
                except Exception:
                    return port, 'filtered'
            
            # Use thread pool for concurrent scanning
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_port = {executor.submit(scan_port, port): port for port in ports}
                
                for future in as_completed(future_to_port):
                    port, status = future.result()
                    results[f'{status}_ports'].append(port)
            
            return AttackResult(
                technique="port_scan",
                target=target,
                success=True,
                data=results,
                timestamp=time.time(),
                mitre_technique="T1046",
                description="Port scan completed"
            )
            
        except Exception as e:
            self.logger.error(f"Port scan failed: {e}")
            return AttackResult(
                technique="port_scan",
                target=target,
                success=False,
                data={'error': str(e)},
                timestamp=time.time(),
                mitre_technique="T1046",
                description=f"Port scan failed: {e}"
            )

class PostExploitationModule:
    """Post-exploitation simulation capabilities"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def lateral_movement_simulation(self, target: str) -> AttackResult:
        """Simulate lateral movement activities"""
        try:
            self.logger.info(f"Starting lateral movement simulation on {target}")
            
            # Simulate various lateral movement techniques
            results = {
                'techniques_simulated': [],
                'successful_movements': [],
                'failed_movements': []
            }
            
            # Simulate SMB enumeration
            try:
                # This would normally use actual SMB commands
                results['techniques_simulated'].append('SMB Enumeration')
                results['successful_movements'].append({
                    'technique': 'SMB Enumeration',
                    'target': target,
                    'details': 'Simulated SMB share enumeration'
                })
            except Exception as e:
                results['failed_movements'].append({
                    'technique': 'SMB Enumeration',
                    'target': target,
                    'error': str(e)
                })
            
            # Simulate WMI execution
            try:
                results['techniques_simulated'].append('WMI Execution')
                results['successful_movements'].append({
                    'technique': 'WMI Execution',
                    'target': target,
                    'details': 'Simulated WMI command execution'
                })
            except Exception as e:
                results['failed_movements'].append({
                    'technique': 'WMI Execution',
                    'target': target,
                    'error': str(e)
                })
            
            return AttackResult(
                technique="lateral_movement",
                target=target,
                success=True,
                data=results,
                timestamp=time.time(),
                mitre_technique="T1021",
                description="Lateral movement simulation completed"
            )
            
        except Exception as e:
            self.logger.error(f"Lateral movement simulation failed: {e}")
            return AttackResult(
                technique="lateral_movement",
                target=target,
                success=False,
                data={'error': str(e)},
                timestamp=time.time(),
                mitre_technique="T1021",
                description=f"Lateral movement simulation failed: {e}"
            )
    
    def persistence_simulation(self, target: str) -> AttackResult:
        """Simulate persistence mechanisms"""
        try:
            self.logger.info(f"Starting persistence simulation on {target}")
            
            results = {
                'techniques_simulated': [],
                'registry_entries': [],
                'scheduled_tasks': [],
                'startup_items': []
            }
            
            # Simulate registry persistence
            results['techniques_simulated'].append('Registry Persistence')
            results['registry_entries'].append({
                'key': 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run',
                'value': 'SimulatedPersistence',
                'data': 'C:\\temp\\malware.exe'
            })
            
            # Simulate scheduled task persistence
            results['techniques_simulated'].append('Scheduled Task Persistence')
            results['scheduled_tasks'].append({
                'name': 'SimulatedTask',
                'command': 'C:\\temp\\malware.exe',
                'trigger': 'At startup'
            })
            
            return AttackResult(
                technique="persistence",
                target=target,
                success=True,
                data=results,
                timestamp=time.time(),
                mitre_technique="T1053",
                description="Persistence simulation completed"
            )
            
        except Exception as e:
            self.logger.error(f"Persistence simulation failed: {e}")
            return AttackResult(
                technique="persistence",
                target=target,
                success=False,
                data={'error': str(e)},
                timestamp=time.time(),
                mitre_technique="T1053",
                description=f"Persistence simulation failed: {e}"
            )
