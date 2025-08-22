#!/usr/bin/env python3
"""
Bluetooth Reconnaissance Module - Phase 1
Comprehensive device discovery and metadata collection using multiple methods:
- PyBluez for Classic Bluetooth
- Bleak for BLE devices  
- PowerShell for adapter information
"""

import asyncio
import json
import csv
import subprocess
import platform
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Optional imports with graceful degradation
try:
    import bluetooth
    PYBLUEZ_AVAILABLE = True
except ImportError:
    PYBLUEZ_AVAILABLE = False
    logging.warning("PyBluez not available. Classic Bluetooth scanning disabled.")

try:
    from bleak import BleakScanner
    BLEAK_AVAILABLE = True
except ImportError:
    BLEAK_AVAILABLE = False
    logging.warning("Bleak not available. BLE scanning disabled.")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BluetoothReconnaissance:
    """Comprehensive Bluetooth reconnaissance system for Phase 1."""
    
    def __init__(self):
        self.results = {
            "scan_info": {
                "timestamp": datetime.now().isoformat(),
                "platform": platform.system(),
                "methods_available": {
                    "pybluez": PYBLUEZ_AVAILABLE,
                    "bleak": BLEAK_AVAILABLE,
                    "powershell": platform.system() == "Windows"
                }
            },
            "adapters": [],
            "devices": {
                "classic": [],
                "ble": [],
                "combined": []
            }
        }
    
    def get_adapter_info_powershell(self) -> List[Dict]:
        """Get Bluetooth adapter information using PowerShell (Windows)."""
        adapters = []
        
        if platform.system() != "Windows":
            logger.warning("PowerShell adapter info only available on Windows")
            return adapters
        
        try:
            # PowerShell command to get Bluetooth adapter information
            ps_command = """
            Get-PnpDevice -Class Bluetooth | ForEach-Object {
                $adapter = @{
                    Name = $_.FriendlyName
                    Status = $_.Status
                    InstanceId = $_.InstanceId
                    Class = $_.Class
                    Manufacturer = $_.Manufacturer
                }
                [PSCustomObject]$adapter
            } | ConvertTo-Json -Depth 3
            """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                adapters_data = json.loads(result.stdout)
                if isinstance(adapters_data, list):
                    adapters = adapters_data
                else:
                    adapters = [adapters_data]
                    
                logger.info(f"Found {len(adapters)} Bluetooth adapters via PowerShell")
            else:
                logger.error(f"PowerShell command failed: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error getting adapter info via PowerShell: {e}")
        
        return adapters
    
    def scan_classic_bluetooth(self, timeout: int = 10) -> List[Dict]:
        """Scan for Classic Bluetooth devices using PyBluez."""
        devices = []
        
        if not PYBLUEZ_AVAILABLE:
            logger.warning("PyBluez not available for Classic Bluetooth scanning")
            return devices
        
        try:
            logger.info(f"Starting Classic Bluetooth scan (timeout: {timeout}s)")
            start_time = time.time()
            
            # Discover nearby devices
            nearby_devices = bluetooth.discover_devices(
                duration=timeout,
                lookup_names=True,
                lookup_class=True,
                device_id=-1,
                inquiry_time=timeout
            )
            
            scan_time = time.time() - start_time
            
            for addr, name, device_class in nearby_devices:
                device_info = {
                    "address": addr,
                    "name": name or "Unknown",
                    "device_class": device_class,
                    "device_type": "Classic",
                    "rssi": None,  # PyBluez doesn't provide RSSI in discovery
                    "scan_time": scan_time,
                    "services": [],
                    "metadata": {
                        "major_class": self._get_major_class(device_class),
                        "minor_class": self._get_minor_class(device_class),
                        "service_class": self._get_service_class(device_class)
                    }
                }
                devices.append(device_info)
                
            logger.info(f"Classic Bluetooth scan completed: {len(devices)} devices found")
            
        except Exception as e:
            logger.error(f"Error during Classic Bluetooth scan: {e}")
        
        return devices
    
    async def scan_ble_devices(self, timeout: int = 10) -> List[Dict]:
        """Scan for BLE devices using Bleak."""
        devices = []
        
        if not BLEAK_AVAILABLE:
            logger.warning("Bleak not available for BLE scanning")
            return devices
        
        try:
            logger.info(f"Starting BLE scan (timeout: {timeout}s)")
            start_time = time.time()
            
            # Discover BLE devices
            scanner = BleakScanner()
            ble_devices = await scanner.discover(timeout=timeout)
            
            scan_time = time.time() - start_time
            
            for device in ble_devices:
                device_info = {
                    "address": device.address,
                    "name": device.name or "Unknown",
                    "device_type": "BLE",
                    "rssi": getattr(device, 'rssi', None),
                    "scan_time": scan_time,
                    "advertisement_data": {
                        "manufacturer_data": dict(getattr(device, 'metadata', {}).get("manufacturer_data", {})),
                        "service_data": dict(getattr(device, 'metadata', {}).get("service_data", {})),
                        "service_uuids": list(getattr(device, 'metadata', {}).get("service_uuids", [])),
                        "tx_power": getattr(device, 'metadata', {}).get("tx_power"),
                        "platform_data": getattr(device, 'metadata', {}).get("platform_data", {})
                    },
                    "metadata": {
                        "discovered_time": getattr(device, 'metadata', {}).get("discovered_time"),
                        "uuids": list(getattr(device, 'metadata', {}).get("uuids", [])),
                        "platform_specific": getattr(device, 'metadata', {}).get("platform_specific", {})
                    }
                }
                devices.append(device_info)
                
            logger.info(f"BLE scan completed: {len(devices)} devices found")
            
        except Exception as e:
            logger.error(f"Error during BLE scan: {e}")
        
        return devices
    
    def _get_major_class(self, device_class: int) -> str:
        """Convert device class to major class name."""
        major_classes = {
            0x00: "Miscellaneous",
            0x01: "Computer",
            0x02: "Phone",
            0x03: "LAN/Network Access Point",
            0x04: "Audio/Video",
            0x05: "Peripheral",
            0x06: "Imaging",
            0x07: "Wearable",
            0x08: "Toy",
            0x09: "Health",
            0x1F: "Uncategorized"
        }
        major = (device_class >> 8) & 0x1F
        return major_classes.get(major, "Unknown")
    
    def _get_minor_class(self, device_class: int) -> str:
        """Convert device class to minor class name."""
        minor = (device_class >> 2) & 0x3F
        return f"Minor Class: {minor}"
    
    def _get_service_class(self, device_class: int) -> str:
        """Convert device class to service class name."""
        service = device_class & 0x3
        service_classes = {
            0: "No services",
            1: "Limited Discoverable Mode",
            2: "Reserved",
            3: "Reserved"
        }
        return service_classes.get(service, "Unknown")
    
    def combine_results(self):
        """Combine all scan results into unified format."""
        all_devices = []
        
        # Add Classic Bluetooth devices
        for device in self.results["devices"]["classic"]:
            device["scan_method"] = "PyBluez"
            all_devices.append(device)
        
        # Add BLE devices
        for device in self.results["devices"]["ble"]:
            device["scan_method"] = "Bleak"
            all_devices.append(device)
        
        # Remove duplicates based on MAC address
        seen_addresses = set()
        unique_devices = []
        
        for device in all_devices:
            addr = device["address"].upper()
            if addr not in seen_addresses:
                seen_addresses.add(addr)
                unique_devices.append(device)
            else:
                # Merge duplicate entries
                existing = next(d for d in unique_devices if d["address"].upper() == addr)
                if device.get("name") and device["name"] != "Unknown":
                    existing["name"] = device["name"]
                if device.get("rssi") is not None:
                    existing["rssi"] = device["rssi"]
        
        self.results["devices"]["combined"] = unique_devices
        
        # Add summary statistics
        self.results["summary"] = {
            "total_devices": len(unique_devices),
            "classic_devices": len(self.results["devices"]["classic"]),
            "ble_devices": len(self.results["devices"]["ble"]),
            "adapters_found": len(self.results["adapters"]),
            "scan_duration": time.time() - time.mktime(datetime.fromisoformat(self.results["scan_info"]["timestamp"].replace('Z', '+00:00')).timetuple())
        }
    
    async def run_full_reconnaissance(self, timeout: int = 15) -> Dict:
        """Run complete reconnaissance scan."""
        logger.info("Starting Phase 1: Bluetooth Reconnaissance")
        
        # Get adapter information
        logger.info("Gathering adapter information...")
        self.results["adapters"] = self.get_adapter_info_powershell()
        
        # Scan for Classic Bluetooth devices
        logger.info("Scanning for Classic Bluetooth devices...")
        self.results["devices"]["classic"] = self.scan_classic_bluetooth(timeout)
        
        # Scan for BLE devices
        logger.info("Scanning for BLE devices...")
        self.results["devices"]["ble"] = await self.scan_ble_devices(timeout)
        
        # Combine and deduplicate results
        self.combine_results()
        
        logger.info(f"Reconnaissance completed: {self.results['summary']['total_devices']} unique devices found")
        return self.results
    
    def save_results_json(self, filename: Optional[str] = None) -> str:
        """Save results to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bluetooth_reconnaissance_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving JSON results: {e}")
            return ""
    
    def save_results_csv(self, filename: Optional[str] = None) -> str:
        """Save results to CSV file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bluetooth_reconnaissance_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    "Address", "Name", "Device Type", "Scan Method", "RSSI",
                    "Major Class", "Minor Class", "Services", "Metadata"
                ])
                
                # Write device data
                for device in self.results["devices"]["combined"]:
                    writer.writerow([
                        device.get("address", ""),
                        device.get("name", ""),
                        device.get("device_type", ""),
                        device.get("scan_method", ""),
                        device.get("rssi", ""),
                        device.get("metadata", {}).get("major_class", ""),
                        device.get("metadata", {}).get("minor_class", ""),
                        len(device.get("services", [])),
                        json.dumps(device.get("metadata", {}))
                    ])
            
            logger.info(f"Results saved to: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving CSV results: {e}")
            return ""

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Bluetooth Reconnaissance - Phase 1")
    parser.add_argument("--timeout", type=int, default=15, help="Scan timeout in seconds")
    parser.add_argument("--output", type=str, help="Output filename (without extension)")
    parser.add_argument("--format", choices=["json", "csv", "both"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    async def run():
        recon = BluetoothReconnaissance()
        results = await recon.run_full_reconnaissance(args.timeout)
        
        # Save results
        if args.format in ["json", "both"]:
            json_file = recon.save_results_json(args.output + ".json" if args.output else None)
            print(f"JSON results: {json_file}")
        
        if args.format in ["csv", "both"]:
            csv_file = recon.save_results_csv(args.output + ".csv" if args.output else None)
            print(f"CSV results: {csv_file}")
        
        # Print summary
        print(f"\nReconnaissance Summary:")
        print(f"Total devices: {results['summary']['total_devices']}")
        print(f"Classic devices: {results['summary']['classic_devices']}")
        print(f"BLE devices: {results['summary']['ble_devices']}")
        print(f"Adapters found: {results['summary']['adapters_found']}")
    
    asyncio.run(run())

if __name__ == "__main__":
    main()
