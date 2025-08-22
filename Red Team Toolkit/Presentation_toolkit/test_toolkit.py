#!/usr/bin/env python3
"""
Test script for DNS Troubleshooting Presentation Toolkit
This script tests the basic functionality without making network changes.
"""

import os
import sys
import platform
import subprocess
from typing import Optional


def test_platform_detection():
    """Test platform detection functionality."""
    print("Testing platform detection...")
    system = platform.system()
    print(f"Detected platform: {system}")
    
    if system == "Windows":
        print("✓ Windows platform detected")
        return "windows"
    elif system == "Linux":
        print("✓ Linux platform detected")
        return "linux"
    else:
        print(f"⚠ Unsupported platform: {system}")
        return None


def test_python_version():
    """Test Python version compatibility."""
    print("\nTesting Python version...")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 6:
        print("✓ Python version is compatible")
        return True
    else:
        print("✗ Python version too old (requires 3.6+)")
        return False


def test_privileges():
    """Test if running with appropriate privileges."""
    print("\nTesting privileges...")
    
    if platform.system() == "Windows":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin:
                print("✓ Running as Administrator")
                return True
            else:
                print("⚠ Not running as Administrator (required for Windows)")
                return False
        except:
            print("⚠ Could not determine admin status")
            return False
    else:
        # Linux/Unix
        is_root = os.geteuid() == 0
        if is_root:
            print("✓ Running as root")
            return True
        else:
            print("⚠ Not running as root (required for Linux)")
            return False


def test_dependencies():
    """Test if required dependencies are available."""
    print("\nTesting dependencies...")
    
    if platform.system() == "Windows":
        # Test Windows dependencies
        dependencies = {
            'nslookup': 'Built-in Windows tool',
            'ping': 'Built-in Windows tool'
        }
        
        for dep, description in dependencies.items():
            try:
                result = subprocess.run(f"where {dep}", shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✓ {dep} found ({description})")
                else:
                    print(f"✗ {dep} not found ({description})")
            except:
                print(f"✗ {dep} not found ({description})")
        
        # Test Wireshark
        tshark_paths = [
            r"C:\Program Files\Wireshark\tshark.exe",
            r"C:\Program Files (x86)\Wireshark\tshark.exe"
        ]
        
        tshark_found = False
        for path in tshark_paths:
            if os.path.exists(path):
                print(f"✓ tshark found at: {path}")
                tshark_found = True
                break
        
        if not tshark_found:
            print("⚠ tshark not found (Wireshark not installed)")
        
    else:
        # Test Linux dependencies
        dependencies = {
            'tshark': 'Wireshark CLI tools',
            'resolvectl': 'systemd-resolved',
            'dig': 'dnsutils package',
            'ping': 'iputils-ping package'
        }
        
        for dep, description in dependencies.items():
            try:
                result = subprocess.run(f"which {dep}", shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✓ {dep} found ({description})")
                else:
                    print(f"✗ {dep} not found ({description})")
            except:
                print(f"✗ {dep} not found ({description})")


def test_network_interface_detection():
    """Test network interface detection."""
    print("\nTesting network interface detection...")
    
    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                "powershell.exe -Command \"Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object -First 1 -ExpandProperty Name\"",
                shell=True, capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                interface = result.stdout.strip()
                print(f"✓ Found network interface: {interface}")
                return True
            else:
                print("✗ Could not detect network interface")
                return False
        except:
            print("✗ Error detecting network interface")
            return False
    else:
        try:
            result = subprocess.run(
                "ip route | grep default | awk '{print $5}'",
                shell=True, capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                interface = result.stdout.strip()
                print(f"✓ Found network interface: {interface}")
                return True
            else:
                print("✗ Could not detect network interface")
                return False
        except:
            print("✗ Error detecting network interface")
            return False


def test_dns_resolution():
    """Test basic DNS resolution."""
    print("\nTesting DNS resolution...")
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run("nslookup google.com", shell=True, capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run("dig google.com +short", shell=True, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✓ DNS resolution working")
            return True
        else:
            print("✗ DNS resolution failed")
            return False
    except:
        print("✗ Error testing DNS resolution")
        return False


def main():
    """Main test function."""
    print("=" * 60)
    print("DNS Troubleshooting Toolkit - System Test")
    print("=" * 60)
    
    tests = [
        ("Platform Detection", test_platform_detection),
        ("Python Version", test_python_version),
        ("Privileges", test_privileges),
        ("Dependencies", test_dependencies),
        ("Network Interface", test_network_interface_detection),
        ("DNS Resolution", test_dns_resolution)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The toolkit should work correctly.")
    else:
        print("⚠ Some tests failed. Please check the issues above.")
    
    print("\nNext steps:")
    if platform.system() == "Windows":
        print("- Run as Administrator: python dns_resolve_windows.py")
    else:
        print("- Run with sudo: sudo python3 dns_resolve.py")


if __name__ == "__main__":
    main()
