#!/usr/bin/env python3
"""
Example Scanner Plugin for Enhanced Red Team Toolkit
Demonstrates plugin system functionality with a custom network scanner.
"""

__version__ = "1.0.0"
__description__ = "Example network scanner plugin demonstrating plugin system"
__author__ = "Red Team Toolkit"
__requires_sandbox__ = True
__category__ = "Network"

import socket
import threading
import time
import logging
from typing import List, Dict, Any
import os

logger = logging.getLogger(__name__)

def scan_ports_custom(target: str, ports: List[int] = None, timeout: float = 1.0) -> Dict[str, Any]:
    """
    Custom port scanner with enhanced features.
    
    Args:
        target: Target host/IP
        ports: List of ports to scan (default: common ports)
        timeout: Connection timeout in seconds
    
    Returns:
        Dictionary with scan results
    """
    if ports is None:
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
    
    logger.info(f"Starting custom port scan on {target}")
    
    results = {
        'target': target,
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'ports_scanned': len(ports),
        'open_ports': [],
        'closed_ports': [],
        'errors': []
    }
    
    def scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                results['open_ports'].append(port)
                logger.info(f"Port {port} is OPEN on {target}")
            else:
                results['closed_ports'].append(port)
                
        except Exception as e:
            error_msg = f"Error scanning port {port}: {e}"
            results['errors'].append(error_msg)
            logger.error(error_msg)
    
    # Use threading for faster scanning
    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    logger.info(f"Custom scan completed. Found {len(results['open_ports'])} open ports")
    return results

def ping_sweep_custom(network: str, timeout: float = 1.0) -> Dict[str, Any]:
    """
    Custom ping sweep for network discovery.
    
    Args:
        network: Network range (e.g., "192.168.1.0/24")
        timeout: Ping timeout in seconds
    
    Returns:
        Dictionary with ping sweep results
    """
    import subprocess
    import ipaddress
    
    logger.info(f"Starting custom ping sweep on {network}")
    
    results = {
        'network': network,
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'hosts_found': [],
        'hosts_down': [],
        'errors': []
    }
    
    try:
        # Parse network
        network_obj = ipaddress.ip_network(network, strict=False)
        
        for ip in network_obj.hosts():
            ip_str = str(ip)
            try:
                # Use ping command
                if os.name == 'nt':  # Windows
                    cmd = ['ping', '-n', '1', '-w', str(int(timeout * 1000)), ip_str]
                else:  # Linux/Mac
                    cmd = ['ping', '-c', '1', '-W', str(int(timeout)), ip_str]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 2)
                
                if result.returncode == 0:
                    results['hosts_found'].append(ip_str)
                    logger.info(f"Host {ip_str} is UP")
                else:
                    results['hosts_down'].append(ip_str)
                    
            except Exception as e:
                error_msg = f"Error pinging {ip_str}: {e}"
                results['errors'].append(error_msg)
                logger.error(error_msg)
                
    except Exception as e:
        error_msg = f"Error parsing network {network}: {e}"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    
    logger.info(f"Ping sweep completed. Found {len(results['hosts_found'])} hosts")
    return results

def service_detector_custom(target: str, port: int) -> Dict[str, Any]:
    """
    Custom service detection with banner grabbing.
    
    Args:
        target: Target host/IP
        port: Port to check
    
    Returns:
        Dictionary with service information
    """
    logger.info(f"Detecting service on {target}:{port}")
    
    results = {
        'target': target,
        'port': port,
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'service': 'unknown',
        'banner': '',
        'version': '',
        'error': None
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((target, port))
        
        # Send a basic probe
        probes = [
            b'\r\n',
            b'GET / HTTP/1.0\r\n\r\n',
            b'SSH-2.0-OpenSSH_8.0\r\n',
            b'\x00'
        ]
        
        for probe in probes:
            try:
                sock.send(probe)
                response = sock.recv(1024)
                if response:
                    results['banner'] = response.decode('utf-8', errors='ignore').strip()
                    break
            except:
                continue
        
        # Try to identify service based on port and banner
        if port == 80 or port == 443:
            results['service'] = 'HTTP/HTTPS'
        elif port == 22:
            results['service'] = 'SSH'
        elif port == 21:
            results['service'] = 'FTP'
        elif port == 23:
            results['service'] = 'Telnet'
        elif port == 25:
            results['service'] = 'SMTP'
        elif port == 53:
            results['service'] = 'DNS'
        elif port == 3306:
            results['service'] = 'MySQL'
        elif port == 5432:
            results['service'] = 'PostgreSQL'
        else:
            results['service'] = 'Unknown'
        
        sock.close()
        logger.info(f"Service detected: {results['service']} on {target}:{port}")
        
    except Exception as e:
        results['error'] = str(e)
        logger.error(f"Error detecting service on {target}:{port}: {e}")
    
    return results

def plugin_info() -> Dict[str, Any]:
    """
    Return plugin information and available functions.
    
    Returns:
        Dictionary with plugin metadata
    """
    return {
        'name': 'example_scanner',
        'version': __version__,
        'description': __description__,
        'author': __author__,
        'category': __category__,
        'functions': [
            'scan_ports_custom',
            'ping_sweep_custom', 
            'service_detector_custom',
            'plugin_info'
        ],
        'examples': {
            'scan_ports_custom': 'scan_ports_custom("192.168.1.1", [80, 443, 22])',
            'ping_sweep_custom': 'ping_sweep_custom("192.168.1.0/24")',
            'service_detector_custom': 'service_detector_custom("192.168.1.1", 80)'
        }
    }
