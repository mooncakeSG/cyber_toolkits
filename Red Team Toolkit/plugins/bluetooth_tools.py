#!/usr/bin/env python3
"""
Bluetooth Tools Plugin for Enhanced Red Team Toolkit
Provides comprehensive Bluetooth scanning, enumeration, and testing capabilities.
Enhanced with CLI interface, BLE support, automated testing, and improved logging.
"""

__version__ = "2.0.0"
__description__ = "Enhanced Bluetooth scanning and testing tools with CLI interface and BLE support"
__author__ = "Red Team Toolkit"
__requires_sandbox__ = True
__category__ = "Bluetooth"

import time
import logging
import subprocess
import re
import json
import csv
import asyncio
import argparse
import sys
import platform
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

# Try to import optional dependencies
try:
    import click
    CLICK_AVAILABLE = True
except ImportError:
    CLICK_AVAILABLE = False

try:
    from bleak import BleakScanner
    BLEAK_AVAILABLE = True
except ImportError:
    BLEAK_AVAILABLE = False

logger = logging.getLogger(__name__)

# Configuration for retry logic
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds

def retry_on_failure(func):
    """Decorator to retry functions on failure."""
    def wrapper(*args, **kwargs):
        last_exception = None
        for attempt in range(RETRY_ATTEMPTS):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                if attempt < RETRY_ATTEMPTS - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                break
        logger.error(f"All {RETRY_ATTEMPTS} attempts failed for {func.__name__}")
        return {"error": str(last_exception), "success": False}
    return wrapper

async def scan_ble_devices(timeout: int = 10) -> Dict[str, Any]:
    """
    Scan for BLE (Bluetooth Low Energy) devices using Bleak.
    
    Args:
        timeout: Scan timeout in seconds
    
    Returns:
        Dictionary containing scan results and metadata
    """
    if not BLEAK_AVAILABLE:
        return {
            "success": False,
            "error": "Bleak library not available. Install with: pip install bleak",
            "devices": [],
            "scan_time": 0,
            "method": "BLE"
        }
    
    start_time = time.time()
    devices = []
    
    try:
        logger.info(f"Starting BLE scan with {timeout}s timeout")
        discovered_devices = await BleakScanner.discover(timeout=timeout)
        
        for device in discovered_devices:
            device_info = {
                "address": device.address,
                "name": device.name or "Unknown",
                "rssi": getattr(device, 'rssi', None),
                "advertisement_data": getattr(device, 'metadata', {}),
                "device_type": "BLE"
            }
            devices.append(device_info)
            logger.info(f"Found BLE device: {device.address} - {device.name}")
        
        scan_time = time.time() - start_time
        
        return {
            "success": True,
            "devices": devices,
            "scan_time": scan_time,
            "method": "BLE",
            "timestamp": datetime.now().isoformat(),
            "total_devices": len(devices)
        }
        
    except Exception as e:
        logger.error(f"BLE scan failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "devices": [],
            "scan_time": time.time() - start_time,
            "method": "BLE"
        }

@retry_on_failure
def scan_bluetooth_devices(timeout: int = 10) -> Dict[str, Any]:
    """
    Scan for nearby Bluetooth devices.
    
    Args:
        timeout: Scan timeout in seconds
    
    Returns:
        Dictionary with discovered devices
    """
    logger.info(f"Starting Bluetooth device scan (timeout: {timeout}s)")
    
    results = {
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'devices_found': [],
        'errors': [],
        'scan_duration': 0
    }
    
    start_time = time.time()
    
    try:
        # Use hcitool for scanning (Linux)
        if Path("/usr/bin/hcitool").exists():
            cmd = ["hcitool", "scan", "--timeout", str(timeout)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
            
            if result.returncode == 0:
                # Parse hcitool output
                lines = result.stdout.strip().split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            mac_address = parts[0].strip()
                            name = parts[1].strip() if len(parts) > 1 else "Unknown"
                            
                            device_info = {
                                'mac_address': mac_address,
                                'name': name,
                                'discovered_at': time.strftime('%Y-%m-%d %H:%M:%S')
                            }
                            results['devices_found'].append(device_info)
                            logger.info(f"Found device: {name} ({mac_address})")
            
            else:
                error_msg = f"hcitool scan failed: {result.stderr}"
                results['errors'].append(error_msg)
                logger.error(error_msg)
        
        # Use bluetoothctl for scanning (Linux)
        elif Path("/usr/bin/bluetoothctl").exists():
            cmd = ["bluetoothctl", "scan", "on"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
            
            if result.returncode == 0:
                # Parse bluetoothctl output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if "Device" in line and ":" in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            mac_address = parts[1]
                            name = " ".join(parts[2:]) if len(parts) > 2 else "Unknown"
                            
                            device_info = {
                                'mac_address': mac_address,
                                'name': name,
                                'discovered_at': time.strftime('%Y-%m-%d %H:%M:%S')
                            }
                            results['devices_found'].append(device_info)
                            logger.info(f"Found device: {name} ({mac_address})")
        
        # Windows Bluetooth scanning
        elif Path("C:/Windows/System32/bthprops.cpl").exists():
            # Use PowerShell to scan for Bluetooth devices
            ps_script = """
            Add-Type -AssemblyName System.Runtime.WindowsRuntime
            $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
            
            Function Await($WinRtTask, $ResultType) {
                $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
                $netTask = $asTask.Invoke($null, @($WinRtTask))
                $netTask.Wait(-1) | Out-Null
                $netTask.Result
            }
            
            Function AwaitWithProgress($WinRtTask, $ResultType, $ProgressCallback) {
                $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
                $netTask = $asTask.Invoke($null, @($WinRtTask))
                $netTask.Progress = $ProgressCallback
                $netTask.Wait(-1) | Out-Null
                $netTask.Result
            }
            
            [Windows.Devices.Enumeration.DeviceInformation, Windows.System.Runtime, ContentType = WindowsRuntime] | Out-Null
            [Windows.Devices.Enumeration.DeviceWatcher, Windows.System.Runtime, ContentType = WindowsRuntime] | Out-Null
            
            $deviceWatcher = [Windows.Devices.Enumeration.DeviceInformation]::CreateWatcher("(System.Devices.Aep.ProtocolId:=\"{e0cbf06c-cd8b-4647-bb8a-263b43f0f974}\")")
            
            $devices = @()
            $deviceWatcher.Add_Added({
                param($sender, $device)
                $deviceInfo = @{
                    'id' = $device.Id
                    'name' = $device.Name
                    'isEnabled' = $device.IsEnabled
                    'isDefault' = $device.IsDefault
                    'kind' = $device.Kind
                }
                $devices += $deviceInfo
            })
            
            $deviceWatcher.Start()
            Start-Sleep -Seconds """ + str(timeout) + """
            $deviceWatcher.Stop()
            
            $devices | ConvertTo-Json
            """
            
            result = subprocess.run(["powershell", "-Command", ps_script], 
                                  capture_output=True, text=True, timeout=timeout + 10)
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    devices_data = json.loads(result.stdout)
                    for device in devices_data:
                        device_info = {
                            'mac_address': device.get('id', 'Unknown'),
                            'name': device.get('name', 'Unknown'),
                            'is_enabled': device.get('isEnabled', False),
                            'is_default': device.get('isDefault', False),
                            'kind': device.get('kind', 'Unknown'),
                            'discovered_at': time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        results['devices_found'].append(device_info)
                        logger.info(f"Found device: {device_info['name']} ({device_info['mac_address']})")
                except json.JSONDecodeError:
                    error_msg = "Failed to parse Windows Bluetooth scan results"
                    results['errors'].append(error_msg)
                    logger.error(error_msg)
            else:
                error_msg = f"Windows Bluetooth scan failed: {result.stderr}"
                results['errors'].append(error_msg)
                logger.error(error_msg)
        
        else:
            error_msg = "No Bluetooth scanning tools found (hcitool, bluetoothctl, or Windows Bluetooth)"
            results['errors'].append(error_msg)
            logger.error(error_msg)
    
    except subprocess.TimeoutExpired:
        error_msg = f"Bluetooth scan timed out after {timeout} seconds"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    except Exception as e:
        error_msg = f"Error during Bluetooth scan: {e}"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    
    results['scan_duration'] = time.time() - start_time
    logger.info(f"Bluetooth scan completed. Found {len(results['devices_found'])} devices")
    
    return results

def get_bluetooth_info() -> Dict[str, Any]:
    """
    Get information about the local Bluetooth adapter.
    
    Returns:
        Dictionary with Bluetooth adapter information
    """
    logger.info("Getting Bluetooth adapter information")
    
    results = {
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'adapter_info': {},
        'errors': []
    }
    
    try:
        # Linux: Use hciconfig
        if Path("/usr/bin/hciconfig").exists():
            cmd = ["hciconfig"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Parse hciconfig output
                lines = result.stdout.strip().split('\n')
                current_adapter = None
                
                for line in lines:
                    if ':' in line and not line.startswith('\t'):
                        # New adapter
                        adapter_name = line.split(':')[0]
                        current_adapter = {
                            'name': adapter_name,
                            'type': 'hci',
                            'status': 'unknown',
                            'address': 'unknown'
                        }
                        results['adapter_info'][adapter_name] = current_adapter
                    
                    elif current_adapter and line.strip():
                        if 'BD Address:' in line:
                            current_adapter['address'] = line.split('BD Address:')[1].strip()
                        elif 'UP RUNNING' in line:
                            current_adapter['status'] = 'up'
                        elif 'DOWN' in line:
                            current_adapter['status'] = 'down'
        
        # Windows: Use PowerShell
        elif Path("C:/Windows/System32/bthprops.cpl").exists():
            ps_script = """
            Get-PnpDevice -Class Bluetooth | Select-Object FriendlyName, Status, InstanceId | ConvertTo-Json
            """
            
            result = subprocess.run(["powershell", "-Command", ps_script], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    devices_data = json.loads(result.stdout)
                    for device in devices_data:
                        adapter_info = {
                            'name': device.get('FriendlyName', 'Unknown'),
                            'type': 'bluetooth',
                            'status': device.get('Status', 'Unknown'),
                            'instance_id': device.get('InstanceId', 'Unknown')
                        }
                        results['adapter_info'][adapter_info['name']] = adapter_info
                except json.JSONDecodeError:
                    error_msg = "Failed to parse Windows Bluetooth adapter information"
                    results['errors'].append(error_msg)
                    logger.error(error_msg)
        
        else:
            error_msg = "No Bluetooth tools found to get adapter information"
            results['errors'].append(error_msg)
            logger.error(error_msg)
    
    except Exception as e:
        error_msg = f"Error getting Bluetooth adapter information: {e}"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    
    logger.info(f"Bluetooth adapter info retrieved. Found {len(results['adapter_info'])} adapters")
    return results

def test_bluetooth_pairing(mac_address: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Test Bluetooth pairing with a device.
    
    Args:
        mac_address: MAC address of the target device
        timeout: Pairing timeout in seconds
    
    Returns:
        Dictionary with pairing test results
    """
    logger.info(f"Testing Bluetooth pairing with {mac_address}")
    
    results = {
        'target_mac': mac_address,
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'pairing_successful': False,
        'pairing_time': 0,
        'errors': [],
        'details': {}
    }
    
    start_time = time.time()
    
    try:
        # Linux: Use bluetoothctl
        if Path("/usr/bin/bluetoothctl").exists():
            # Try to pair with the device
            pair_script = f"""
            bluetoothctl << EOF
            pair {mac_address}
            EOF
            """
            
            result = subprocess.run(["bash", "-c", pair_script], 
                                  capture_output=True, text=True, timeout=timeout + 5)
            
            if result.returncode == 0:
                output = result.stdout.lower()
                if "successful" in output or "paired" in output:
                    results['pairing_successful'] = True
                    results['details']['method'] = 'bluetoothctl'
                    results['details']['output'] = result.stdout
                    logger.info(f"Successfully paired with {mac_address}")
                else:
                    results['details']['method'] = 'bluetoothctl'
                    results['details']['output'] = result.stdout
                    results['details']['error'] = result.stderr
                    logger.warning(f"Failed to pair with {mac_address}")
            else:
                error_msg = f"bluetoothctl pairing failed: {result.stderr}"
                results['errors'].append(error_msg)
                logger.error(error_msg)
        
        # Windows: Use PowerShell
        elif Path("C:/Windows/System32/bthprops.cpl").exists():
            ps_script = f"""
            Add-Type -AssemblyName System.Runtime.WindowsRuntime
            $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? {{ $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' }})[0]
            
            Function Await($WinRtTask, $ResultType) {{
                $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
                $netTask = $asTask.Invoke($null, @($WinRtTask))
                $netTask.Wait(-1) | Out-Null
                $netTask.Result
            }}
            
            [Windows.Devices.Bluetooth.BluetoothDevice, Windows.System.Runtime, ContentType = WindowsRuntime] | Out-Null
            
            try {{
                $device = Await([Windows.Devices.Bluetooth.BluetoothDevice]::FromBluetoothAddressAsync("{mac_address}")) ([Windows.Devices.Bluetooth.BluetoothDevice])
                $result = "Device found: " + $device.Name
                $result
            }} catch {{
                $result = "Error: " + $_.Exception.Message
                $result
            }}
            """
            
            result = subprocess.run(["powershell", "-Command", ps_script], 
                                  capture_output=True, text=True, timeout=timeout + 5)
            
            if result.returncode == 0:
                output = result.stdout.lower()
                if "device found" in output:
                    results['pairing_successful'] = True
                    results['details']['method'] = 'powershell'
                    results['details']['output'] = result.stdout
                    logger.info(f"Successfully connected to {mac_address}")
                else:
                    results['details']['method'] = 'powershell'
                    results['details']['output'] = result.stdout
                    results['details']['error'] = result.stderr
                    logger.warning(f"Failed to connect to {mac_address}")
            else:
                error_msg = f"Windows Bluetooth connection failed: {result.stderr}"
                results['errors'].append(error_msg)
                logger.error(error_msg)
        
        else:
            error_msg = "No Bluetooth tools found for pairing test"
            results['errors'].append(error_msg)
            logger.error(error_msg)
    
    except subprocess.TimeoutExpired:
        error_msg = f"Bluetooth pairing test timed out after {timeout} seconds"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    except Exception as e:
        error_msg = f"Error during Bluetooth pairing test: {e}"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    
    results['pairing_time'] = time.time() - start_time
    return results

def enumerate_bluetooth_services(mac_address: str, timeout: int = 15) -> Dict[str, Any]:
    """
    Enumerate Bluetooth services on a device.
    
    Args:
        mac_address: MAC address of the target device
        timeout: Service enumeration timeout in seconds
    
    Returns:
        Dictionary with discovered services
    """
    logger.info(f"Enumerating Bluetooth services on {mac_address}")
    
    results = {
        'target_mac': mac_address,
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'services_found': [],
        'errors': [],
        'scan_duration': 0
    }
    
    start_time = time.time()
    
    try:
        # Linux: Use sdptool
        if Path("/usr/bin/sdptool").exists():
            cmd = ["sdptool", "browse", mac_address]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
            
            if result.returncode == 0:
                # Parse sdptool output
                lines = result.stdout.strip().split('\n')
                current_service = None
                
                for line in lines:
                    if 'Service Name:' in line:
                        service_name = line.split('Service Name:')[1].strip()
                        current_service = {
                            'name': service_name,
                            'uuid': 'unknown',
                            'port': 'unknown',
                            'protocol': 'unknown'
                        }
                        results['services_found'].append(current_service)
                    
                    elif current_service and 'Service RecHandle:' in line:
                        current_service['handle'] = line.split('Service RecHandle:')[1].strip()
                    
                    elif current_service and 'Service Class ID List:' in line:
                        uuid_match = re.search(r'UUID 16: ([0-9a-fA-F]{4})', line)
                        if uuid_match:
                            current_service['uuid'] = uuid_match.group(1)
                    
                    elif current_service and 'Protocol Descriptor List:' in line:
                        port_match = re.search(r'port: ([0-9]+)', line)
                        if port_match:
                            current_service['port'] = port_match.group(1)
                        
                        if 'L2CAP' in line:
                            current_service['protocol'] = 'L2CAP'
                        elif 'RFCOMM' in line:
                            current_service['protocol'] = 'RFCOMM'
            
            else:
                error_msg = f"sdptool browse failed: {result.stderr}"
                results['errors'].append(error_msg)
                logger.error(error_msg)
        
        # Alternative: Use bluetoothctl
        elif Path("/usr/bin/bluetoothctl").exists():
            info_script = f"""
            bluetoothctl << EOF
            info {mac_address}
            EOF
            """
            
            result = subprocess.run(["bash", "-c", info_script], 
                                  capture_output=True, text=True, timeout=timeout + 5)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'UUID:' in line:
                        uuid = line.split('UUID:')[1].strip()
                        service_info = {
                            'name': f"Service-{len(results['services_found']) + 1}",
                            'uuid': uuid,
                            'port': 'unknown',
                            'protocol': 'unknown'
                        }
                        results['services_found'].append(service_info)
        
        else:
            error_msg = "No Bluetooth service enumeration tools found"
            results['errors'].append(error_msg)
            logger.error(error_msg)
    
    except subprocess.TimeoutExpired:
        error_msg = f"Bluetooth service enumeration timed out after {timeout} seconds"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    except Exception as e:
        error_msg = f"Error during Bluetooth service enumeration: {e}"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    
    results['scan_duration'] = time.time() - start_time
    logger.info(f"Bluetooth service enumeration completed. Found {len(results['services_found'])} services")
    
    return results

def bluetooth_security_scan(mac_address: str) -> Dict[str, Any]:
    """
    Perform security analysis of a Bluetooth device.
    
    Args:
        mac_address: MAC address of the target device
    
    Returns:
        Dictionary with security analysis results
    """
    logger.info(f"Performing Bluetooth security scan on {mac_address}")
    
    results = {
        'target_mac': mac_address,
        'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'security_issues': [],
        'recommendations': [],
        'errors': []
    }
    
    try:
        # Get device information first
        device_info = get_bluetooth_info()
        
        # Check for common security issues
        security_checks = [
            {
                'name': 'Bluetooth Visibility',
                'description': 'Check if device is discoverable',
                'risk': 'Medium',
                'recommendation': 'Disable discoverable mode when not needed'
            },
            {
                'name': 'Pairing Security',
                'description': 'Check if device requires pairing',
                'risk': 'High',
                'recommendation': 'Enable pairing requirement for all connections'
            },
            {
                'name': 'Encryption',
                'description': 'Check if communications are encrypted',
                'risk': 'High',
                'recommendation': 'Enable encryption for all Bluetooth communications'
            },
            {
                'name': 'Authentication',
                'description': 'Check if device requires authentication',
                'risk': 'Medium',
                'recommendation': 'Enable authentication for device connections'
            }
        ]
        
        # Add security checks based on available information
        for check in security_checks:
            results['security_issues'].append({
                'issue': check['name'],
                'description': check['description'],
                'risk_level': check['risk'],
                'status': 'Unknown (requires manual verification)',
                'recommendation': check['recommendation']
            })
        
        # Add general recommendations
        results['recommendations'] = [
            'Keep Bluetooth disabled when not in use',
            'Use strong PIN codes for pairing',
            'Regularly update Bluetooth drivers and firmware',
            'Monitor for unauthorized connections',
            'Use Bluetooth Low Energy (BLE) when possible for better security'
        ]
        
        logger.info(f"Bluetooth security scan completed for {mac_address}")
    
    except Exception as e:
        error_msg = f"Error during Bluetooth security scan: {e}"
        results['errors'].append(error_msg)
        logger.error(error_msg)
    
    return results

def save_results_to_json(results: Dict[str, Any], filename: str = None) -> str:
    """
    Save scan results to JSON file.
    
    Args:
        results: Results dictionary to save
        filename: Optional custom filename
    
    Returns:
        Path to saved file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bluetooth_scan_{timestamp}.json"
    
    filepath = Path(filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"Results saved to {filepath}")
        return str(filepath)
    except Exception as e:
        logger.error(f"Failed to save results to JSON: {e}")
        return ""

def save_results_to_csv(results: Dict[str, Any], filename: str = None) -> str:
    """
    Save scan results to CSV file.
    
    Args:
        results: Results dictionary to save
        filename: Optional custom filename
    
    Returns:
        Path to saved file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bluetooth_scan_{timestamp}.csv"
    
    filepath = Path(filename)
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if 'devices' in results and results['devices']:
                # Get all unique keys from all devices
                fieldnames = set()
                for device in results['devices']:
                    fieldnames.update(device.keys())
                fieldnames = sorted(list(fieldnames))
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results['devices'])
            else:
                # Write basic info if no devices found
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'method', 'success', 'total_devices'])
                writer.writerow([
                    results.get('timestamp', ''),
                    results.get('method', ''),
                    results.get('success', ''),
                    results.get('total_devices', 0)
                ])
        
        logger.info(f"Results saved to {filepath}")
        return str(filepath)
    except Exception as e:
        logger.error(f"Failed to save results to CSV: {e}")
        return ""

def automated_discovery_and_test(timeout: int = 10, test_pairing: bool = False, 
                                enumerate_services: bool = False) -> Dict[str, Any]:
    """
    Automated discovery and testing of Bluetooth devices.
    
    Args:
        timeout: Scan timeout in seconds
        test_pairing: Whether to test pairing with discovered devices
        enumerate_services: Whether to enumerate services on discovered devices
    
    Returns:
        Dictionary with comprehensive results
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "success": True,
        "discovery_results": {},
        "pairing_results": [],
        "service_results": [],
        "security_results": [],
        "errors": []
    }
    
    try:
        # Step 1: Discovery
        logger.info("Starting automated Bluetooth discovery")
        discovery_results = scan_bluetooth_devices(timeout)
        results["discovery_results"] = discovery_results
        
        if not discovery_results.get("success", False):
            results["success"] = False
            results["errors"].append("Discovery failed")
            return results
        
        devices = discovery_results.get("devices", [])
        logger.info(f"Found {len(devices)} devices for automated testing")
        
        # Step 2: Automated testing for each device
        for device in devices:
            mac_address = device.get("address", "")
            if not mac_address:
                continue
            
            logger.info(f"Processing device: {mac_address}")
            
            # Test pairing if requested
            if test_pairing:
                try:
                    pairing_result = test_bluetooth_pairing(mac_address, timeout=30)
                    pairing_result["device_address"] = mac_address
                    pairing_result["device_name"] = device.get("name", "Unknown")
                    results["pairing_results"].append(pairing_result)
                except Exception as e:
                    logger.error(f"Pairing test failed for {mac_address}: {e}")
                    results["errors"].append(f"Pairing test failed for {mac_address}: {e}")
            
            # Enumerate services if requested
            if enumerate_services:
                try:
                    service_result = enumerate_bluetooth_services(mac_address, timeout=15)
                    service_result["device_address"] = mac_address
                    service_result["device_name"] = device.get("name", "Unknown")
                    results["service_results"].append(service_result)
                except Exception as e:
                    logger.error(f"Service enumeration failed for {mac_address}: {e}")
                    results["errors"].append(f"Service enumeration failed for {mac_address}: {e}")
            
            # Perform security scan
            try:
                security_result = bluetooth_security_scan(mac_address)
                security_result["device_address"] = mac_address
                security_result["device_name"] = device.get("name", "Unknown")
                results["security_results"].append(security_result)
            except Exception as e:
                logger.error(f"Security scan failed for {mac_address}: {e}")
                results["errors"].append(f"Security scan failed for {mac_address}: {e}")
        
        logger.info("Automated Bluetooth testing completed")
        
    except Exception as e:
        results["success"] = False
        results["errors"].append(f"Automated testing failed: {e}")
        logger.error(f"Automated testing failed: {e}")
    
    return results

def enhanced_security_check(mac_address: str) -> Dict[str, Any]:
    """
    Enhanced security check for Bluetooth devices.
    
    Args:
        mac_address: MAC address of the target device
    
    Returns:
        Dictionary with enhanced security analysis
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "target": mac_address,
        "success": True,
        "encryption_status": "Unknown",
        "authentication_required": "Unknown",
        "vulnerable_services": [],
        "security_score": 0,
        "recommendations": [],
        "errors": []
    }
    
    try:
        # Get basic device info
        device_info = get_bluetooth_info()
        
        # Perform service enumeration
        services = enumerate_bluetooth_services(mac_address)
        
        # Analyze services for security vulnerabilities
        if services.get("success") and services.get("services"):
            for service in services["services"]:
                service_name = service.get("name", "").lower()
                
                # Check for potentially vulnerable services
                vulnerable_patterns = [
                    "obex", "ftp", "dun", "dialup", "hid", "a2dp", "headset"
                ]
                
                for pattern in vulnerable_patterns:
                    if pattern in service_name:
                        results["vulnerable_services"].append({
                            "service": service_name,
                            "uuid": service.get("uuid", ""),
                            "risk": "Medium",
                            "description": f"Service {service_name} may have security implications"
                        })
        
        # Calculate security score (0-100)
        score = 100
        
        # Deduct points for vulnerable services
        score -= len(results["vulnerable_services"]) * 15
        
        # Ensure score doesn't go below 0
        results["security_score"] = max(0, score)
        
        # Generate recommendations
        if results["vulnerable_services"]:
            results["recommendations"].extend([
                "Review exposed services and disable unnecessary ones",
                "Ensure all services use proper authentication",
                "Monitor for unauthorized access attempts"
            ])
        
        results["recommendations"].extend([
            "Keep Bluetooth firmware updated",
            "Use strong pairing methods (avoid legacy PIN)",
            "Implement proper access controls",
            "Regular security audits recommended"
        ])
        
        logger.info(f"Enhanced security check completed for {mac_address}")
        
    except Exception as e:
        results["success"] = False
        results["errors"].append(f"Enhanced security check failed: {e}")
        logger.error(f"Enhanced security check failed: {e}")
    
    return results

def plugin_info() -> Dict[str, Any]:
    """
    Return plugin information and available functions.
    
    Returns:
        Dictionary with plugin metadata
    """
    return {
        'name': 'bluetooth_tools',
        'version': __version__,
        'description': __description__,
        'author': __author__,
        'category': __category__,
        'functions': [
            'scan_bluetooth_devices',
            'scan_ble_devices',
            'get_bluetooth_info',
            'test_bluetooth_pairing',
            'enumerate_bluetooth_services',
            'bluetooth_security_scan',
            'enhanced_security_check',
            'automated_discovery_and_test',
            'save_results_to_json',
            'save_results_to_csv',
            'plugin_info'
        ],
        'examples': {
            'scan_bluetooth_devices': 'scan_bluetooth_devices(timeout=10)',
            'scan_ble_devices': 'await scan_ble_devices(timeout=10)',
            'get_bluetooth_info': 'get_bluetooth_info()',
            'test_bluetooth_pairing': 'test_bluetooth_pairing("00:11:22:33:44:55")',
            'enumerate_bluetooth_services': 'enumerate_bluetooth_services("00:11:22:33:44:55")',
            'bluetooth_security_scan': 'bluetooth_security_scan("00:11:22:33:44:55")',
            'automated_discovery_and_test': 'automated_discovery_and_test(timeout=10, test_pairing=True)',
            'save_results_to_json': 'save_results_to_json(results, "bluetooth_scan.json")'
        }
    }

# CLI Interface Implementation
def setup_cli():
    """Setup command line interface using argparse."""
    parser = argparse.ArgumentParser(
        description="Bluetooth Tools - Enhanced Bluetooth scanning and testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s scan --timeout 15
  %(prog)s scan --ble --output bluetooth_scan.json
  %(prog)s pair --mac 00:11:22:33:44:55 --timeout 30
  %(prog)s services --mac 00:11:22:33:44:55 --output services.csv
  %(prog)s security --mac 00:11:22:33:44:55
  %(prog)s auto --timeout 10 --test-pairing --enumerate-services
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan for Bluetooth devices')
    scan_parser.add_argument('--timeout', type=int, default=10, help='Scan timeout in seconds (default: 10)')
    scan_parser.add_argument('--ble', action='store_true', help='Use BLE scanning (requires bleak)')
    scan_parser.add_argument('--output', help='Output file (JSON or CSV based on extension)')
    
    # Pair command
    pair_parser = subparsers.add_parser('pair', help='Test Bluetooth pairing')
    pair_parser.add_argument('--mac', required=True, help='Target MAC address')
    pair_parser.add_argument('--timeout', type=int, default=30, help='Pairing timeout in seconds (default: 30)')
    pair_parser.add_argument('--output', help='Output file (JSON or CSV based on extension)')
    
    # Services command
    services_parser = subparsers.add_parser('services', help='Enumerate Bluetooth services')
    services_parser.add_argument('--mac', required=True, help='Target MAC address')
    services_parser.add_argument('--timeout', type=int, default=15, help='Enumeration timeout in seconds (default: 15)')
    services_parser.add_argument('--output', help='Output file (JSON or CSV based on extension)')
    
    # Security command
    security_parser = subparsers.add_parser('security', help='Perform security analysis')
    security_parser.add_argument('--mac', required=True, help='Target MAC address')
    security_parser.add_argument('--enhanced', action='store_true', help='Use enhanced security check')
    security_parser.add_argument('--output', help='Output file (JSON or CSV based on extension)')
    
    # Auto command
    auto_parser = subparsers.add_parser('auto', help='Automated discovery and testing')
    auto_parser.add_argument('--timeout', type=int, default=10, help='Scan timeout in seconds (default: 10)')
    auto_parser.add_argument('--test-pairing', action='store_true', help='Test pairing with discovered devices')
    auto_parser.add_argument('--enumerate-services', action='store_true', help='Enumerate services on discovered devices')
    auto_parser.add_argument('--output', help='Output file (JSON or CSV based on extension)')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get Bluetooth adapter information')
    info_parser.add_argument('--output', help='Output file (JSON or CSV based on extension)')
    
    return parser

def save_output(results: Dict[str, Any], output_file: str) -> bool:
    """
    Save results to file based on extension.
    
    Args:
        results: Results to save
        output_file: Output file path
    
    Returns:
        True if successful, False otherwise
    """
    if not output_file:
        return False
    
    try:
        file_path = Path(output_file)
        extension = file_path.suffix.lower()
        
        if extension == '.json':
            return bool(save_results_to_json(results, output_file))
        elif extension == '.csv':
            return bool(save_results_to_csv(results, output_file))
        else:
            # Default to JSON
            json_file = file_path.with_suffix('.json')
            return bool(save_results_to_json(results, str(json_file)))
    except Exception as e:
        logger.error(f"Failed to save output: {e}")
        return False

async def main_cli():
    """Main CLI function."""
    parser = setup_cli()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    results = {}
    
    try:
        if args.command == 'scan':
            if args.ble:
                results = await scan_ble_devices(args.timeout)
            else:
                results = scan_bluetooth_devices(args.timeout)
        
        elif args.command == 'pair':
            results = test_bluetooth_pairing(args.mac, args.timeout)
        
        elif args.command == 'services':
            results = enumerate_bluetooth_services(args.mac, args.timeout)
        
        elif args.command == 'security':
            if args.enhanced:
                results = enhanced_security_check(args.mac)
            else:
                results = bluetooth_security_scan(args.mac)
        
        elif args.command == 'auto':
            results = automated_discovery_and_test(
                timeout=args.timeout,
                test_pairing=args.test_pairing,
                enumerate_services=args.enumerate_services
            )
        
        elif args.command == 'info':
            results = get_bluetooth_info()
        
        # Print results
        print(json.dumps(results, indent=2))
        
        # Save output if specified
        if hasattr(args, 'output') and args.output:
            if save_output(results, args.output):
                print(f"\nResults saved to: {args.output}")
            else:
                print(f"\nFailed to save results to: {args.output}")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"CLI execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(main_cli())
