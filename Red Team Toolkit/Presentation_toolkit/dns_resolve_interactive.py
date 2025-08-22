#!/usr/bin/env python3
"""
Interactive DNS Troubleshooter Simulation Toolkit
A fully interactive, CLI-based tool for demonstrating DNS troubleshooting with automatic setup.
"""

import os
import sys
import subprocess
import time
import signal
import threading
import platform
import shutil
from typing import Optional, List, Dict


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.ENDC}\n")


def print_step(step_num: int, title: str):
    """Print a formatted step header."""
    print(f"{Colors.OKBLUE}{Colors.BOLD}[Step {step_num}] {title}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'-' * (len(title) + 10)}{Colors.ENDC}")


def print_success(message: str):
    """Print a success message."""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print an error message."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print an info message."""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def get_user_input(prompt: str, default: str = "", required: bool = True) -> str:
    """Get user input with validation."""
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                user_input = default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if not required or user_input:
            return user_input
        else:
            print_error("This field is required. Please enter a value.")


def get_user_choice(prompt: str, options: List[str], default: int = 0) -> int:
    """Get user choice from a list of options."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        marker = "→" if i == default + 1 else " "
        print(f"  {marker} {i}. {option}")
    
    while True:
        try:
            choice = input(f"\nSelect option (1-{len(options)}, default {default + 1}): ").strip()
            if not choice:
                return default
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return choice_num - 1
            else:
                print_error(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print_error("Please enter a valid number")


def confirm_action(prompt: str, default: bool = True) -> bool:
    """Get user confirmation for an action."""
    default_text = "Y/n" if default else "y/N"
    while True:
        response = input(f"{prompt} ({default_text}): ").strip().lower()
        if not response:
            return default
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print_error("Please enter 'y' or 'n'")


def run_command(command: str, capture_output: bool = False, timeout: int = 30) -> Optional[str]:
    """Run a shell command and return output if requested."""
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
            return result.stdout.strip() if result.returncode == 0 else None
        else:
            subprocess.run(command, shell=True, check=True, timeout=timeout)
            return None
    except subprocess.TimeoutExpired:
        print_error(f"Command timed out: {command}")
        return None
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {command}")
        return None
    except Exception as e:
        print_error(f"Error running command: {e}")
        return None


def install_wireshark_linux():
    """Install Wireshark on Linux systems."""
    print_info("Installing Wireshark CLI tools...")
    
    # Detect package manager
    if shutil.which("apt-get"):
        package_manager = "apt"
        install_cmd = "sudo apt-get update && sudo apt-get install -y wireshark-cli"
    elif shutil.which("yum"):
        package_manager = "yum"
        install_cmd = "sudo yum install -y wireshark-cli"
    elif shutil.which("dnf"):
        package_manager = "dnf"
        install_cmd = "sudo dnf install -y wireshark-cli"
    else:
        print_error("Could not detect package manager (apt, yum, or dnf)")
        return False
    
    print_info(f"Using {package_manager} package manager")
    
    if run_command(install_cmd):
        print_success("Wireshark CLI tools installed successfully")
        return True
    else:
        print_error("Failed to install Wireshark CLI tools")
        return False


def install_wireshark_windows():
    """Install Wireshark on Windows systems."""
    print_info("Wireshark installation for Windows requires manual download")
    print_info("Please visit: https://www.wireshark.org/download.html")
    print_info("Download and install Wireshark, then restart this script")
    
    if confirm_action("Open Wireshark download page in browser?", True):
        import webbrowser
        webbrowser.open("https://www.wireshark.org/download.html")
    
    return False


def check_and_install_dependencies():
    """Check and install missing dependencies."""
    print_step(1, "Checking Dependencies")
    
    if platform.system() == "Windows":
        return check_and_install_dependencies_windows()
    else:
        return check_and_install_dependencies_linux()


def check_and_install_dependencies_linux():
    """Check and install dependencies on Linux."""
    dependencies = {
        'tshark': 'Wireshark CLI tools',
        'resolvectl': 'systemd-resolved',
        'dig': 'dnsutils package',
        'ping': 'iputils-ping package'
    }
    
    missing = []
    
    for dep, description in dependencies.items():
        if not shutil.which(dep):
            missing.append((dep, description))
        else:
            print_success(f"{dep} found ({description})")
    
    if missing:
        print_warning(f"Missing dependencies: {', '.join([dep for dep, _ in missing])}")
        
        if confirm_action("Install missing dependencies automatically?", True):
            for dep, description in missing:
                if dep == 'tshark':
                    if not install_wireshark_linux():
                        return False
                else:
                    print_info(f"Installing {dep}...")
                    if platform.system() == "Linux":
                        if shutil.which("apt-get"):
                            install_cmd = f"sudo apt-get install -y {dep}"
                        elif shutil.which("yum"):
                            install_cmd = f"sudo yum install -y {dep}"
                        elif shutil.which("dnf"):
                            install_cmd = f"sudo dnf install -y {dep}"
                        else:
                            print_error(f"Could not install {dep} automatically")
                            return False
                        
                        if not run_command(install_cmd):
                            print_error(f"Failed to install {dep}")
                            return False
                        else:
                            print_success(f"{dep} installed successfully")
        else:
            print_error("Cannot continue without required dependencies")
            return False
    
    return True


def check_and_install_dependencies_windows():
    """Check and install dependencies on Windows."""
    dependencies = {
        'nslookup': 'Built-in Windows tool',
        'ping': 'Built-in Windows tool'
    }
    
    missing = []
    
    for dep, description in dependencies.items():
        if not shutil.which(dep):
            missing.append((dep, description))
        else:
            print_success(f"{dep} found ({description})")
    
    # Check for Wireshark
    tshark_paths = [
        r"C:\Program Files\Wireshark\tshark.exe",
        r"C:\Program Files (x86)\Wireshark\tshark.exe"
    ]
    
    tshark_found = any(os.path.exists(path) for path in tshark_paths)
    if tshark_found:
        print_success("tshark found (Wireshark CLI tools)")
    else:
        missing.append(('tshark', 'Wireshark CLI tools'))
    
    if missing:
        print_warning(f"Missing dependencies: {', '.join([dep for dep, _ in missing])}")
        
        if confirm_action("Install missing dependencies automatically?", True):
            for dep, description in missing:
                if dep == 'tshark':
                    if not install_wireshark_windows():
                        return False
                else:
                    print_error(f"Cannot install {dep} automatically on Windows")
                    return False
        else:
            print_error("Cannot continue without required dependencies")
            return False
    
    return True


def get_network_interface() -> Optional[str]:
    """Get the active network interface with user selection."""
    print_info("Detecting network interfaces...")
    
    if platform.system() == "Windows":
        return get_network_interface_windows()
    else:
        return get_network_interface_linux()


def get_network_interface_linux() -> Optional[str]:
    """Get network interface on Linux with user selection."""
    try:
        # Get all network interfaces
        result = run_command("ip link show | grep -E '^[0-9]+:' | awk -F': ' '{print $2}'", True)
        if not result:
            print_error("Could not detect network interfaces")
            return None
        
        interfaces = [iface.strip() for iface in result.split('\n') if iface.strip()]
        
        if not interfaces:
            print_error("No network interfaces found")
            return None
        
        # Filter out loopback and down interfaces
        active_interfaces = []
        for iface in interfaces:
            if iface != 'lo':  # Skip loopback
                # Check if interface is up
                status_result = run_command(f"ip link show {iface} | grep -q 'state UP'", True)
                if status_result is not None:
                    active_interfaces.append(iface)
        
        if not active_interfaces:
            active_interfaces = interfaces  # Fallback to all interfaces
        
        if len(active_interfaces) == 1:
            interface = active_interfaces[0]
            print_success(f"Using interface: {interface}")
            return interface
        
        # Let user choose
        print_info("Multiple network interfaces detected:")
        for i, iface in enumerate(active_interfaces):
            print(f"  {i+1}. {iface}")
        
        choice = get_user_choice("Select network interface:", active_interfaces, 0)
        selected_interface = active_interfaces[choice]
        
        print_success(f"Selected interface: {selected_interface}")
        return selected_interface
        
    except Exception as e:
        print_error(f"Error getting network interface: {e}")
        return None


def get_network_interface_windows() -> Optional[str]:
    """Get network interface on Windows with user selection."""
    try:
        # Get network adapters using PowerShell
        result = run_command(
            "powershell.exe -Command \"Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object Name, InterfaceDescription | ConvertTo-Json\"",
            True
        )
        
        if not result:
            print_error("Could not detect network interfaces")
            return None
        
        # Parse JSON output (simplified)
        interfaces = []
        lines = result.split('\n')
        current_name = None
        
        for line in lines:
            if '"Name"' in line:
                current_name = line.split('"Name":')[1].strip().strip('",')
            elif '"InterfaceDescription"' in line and current_name:
                interfaces.append(current_name)
                current_name = None
        
        if not interfaces:
            # Fallback: get all interfaces
            result = run_command(
                "powershell.exe -Command \"Get-NetAdapter | Select-Object -ExpandProperty Name\"",
                True
            )
            if result:
                interfaces = [iface.strip() for iface in result.split('\n') if iface.strip()]
        
        if not interfaces:
            print_error("No network interfaces found")
            return None
        
        if len(interfaces) == 1:
            interface = interfaces[0]
            print_success(f"Using interface: {interface}")
            return interface
        
        # Let user choose
        print_info("Multiple network interfaces detected:")
        for i, iface in enumerate(interfaces):
            print(f"  {i+1}. {iface}")
        
        choice = get_user_choice("Select network interface:", interfaces, 0)
        selected_interface = interfaces[choice]
        
        print_success(f"Selected interface: {selected_interface}")
        return selected_interface
        
    except Exception as e:
        print_error(f"Error getting network interface: {e}")
        return None


def configure_simulation():
    """Configure simulation parameters interactively."""
    print_step(2, "Configuration")
    
    # Get target domain
    target_domain = get_user_input("Enter target domain for testing", "google.com")
    
    # Get DNS servers
    print_info("DNS server configuration:")
    bad_dns = get_user_input("Enter invalid DNS server IP", "123.123.123.123")
    good_dns = get_user_input("Enter working DNS server IP", "8.8.8.8")
    
    # Get capture settings
    capture_duration = get_user_input("Enter capture duration in seconds", "30")
    try:
        capture_duration = int(capture_duration)
    except ValueError:
        capture_duration = 30
    
    # Get capture file name
    capture_file = get_user_input("Enter capture file name", "dns_capture.pcap")
    
    return {
        'target_domain': target_domain,
        'bad_dns': bad_dns,
        'good_dns': good_dns,
        'capture_duration': capture_duration,
        'capture_file': capture_file
    }


def display_network_info(interface: str, config: Dict):
    """Display current network information."""
    print_step(3, "Network Information")
    
    print(f"{Colors.OKCYAN}Network Interface: {interface}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Target Domain: {config['target_domain']}{Colors.ENDC}")
    
    if platform.system() == "Windows":
        # Show interface details
        print(f"\n{Colors.BOLD}Interface Details:{Colors.ENDC}")
        run_command(f"powershell.exe -Command \"Get-NetAdapter -Name '{interface}' | Format-List\"")
        
        # Show IP configuration
        print(f"\n{Colors.BOLD}IP Configuration:{Colors.ENDC}")
        run_command(f"powershell.exe -Command \"Get-NetIPAddress -InterfaceAlias '{interface}' | Format-Table\"")
        
        # Show DNS configuration
        print(f"\n{Colors.BOLD}DNS Configuration:{Colors.ENDC}")
        run_command(f"powershell.exe -Command \"Get-DnsClientServerAddress -InterfaceAlias '{interface}' | Format-Table\"")
    else:
        # Show interface details
        print(f"\n{Colors.BOLD}Interface Details:{Colors.ENDC}")
        run_command(f"ip addr show {interface}")
        
        # Show DNS configuration
        print(f"\n{Colors.BOLD}DNS Configuration:{Colors.ENDC}")
        run_command("cat /etc/resolv.conf")
        
        # Show current DNS servers
        print(f"\n{Colors.BOLD}Current DNS Servers:{Colors.ENDC}")
        run_command("resolvectl status")


def start_wireshark_capture(interface: str, capture_file: str) -> Optional[int]:
    """Start Wireshark capture in background."""
    print_step(4, "Starting Wireshark Capture")
    
    print(f"Starting capture on interface: {interface}")
    print(f"Capture file: {capture_file}")
    
    try:
        if platform.system() == "Windows":
            # Find tshark path
            tshark_paths = [
                r"C:\Program Files\Wireshark\tshark.exe",
                r"C:\Program Files (x86)\Wireshark\tshark.exe"
            ]
            tshark_path = None
            for path in tshark_paths:
                if os.path.exists(path):
                    tshark_path = path
                    break
            
            if not tshark_path:
                print_error("tshark not found. Please install Wireshark.")
                return None
            
            # Start tshark in background
            process = subprocess.Popen(
                f'"{tshark_path}" -i "{interface}" -w "{capture_file}" -f "port 53"',
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        else:
            # Start tshark in background
            process = subprocess.Popen(
                f"sudo tshark -i {interface} -w {capture_file} -f 'port 53'",
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        
        # Wait a moment for capture to start
        time.sleep(2)
        
        if process.poll() is None:  # Process is still running
            print_success("Wireshark capture started successfully")
            return process.pid
        else:
            print_error("Failed to start Wireshark capture")
            return None
            
    except Exception as e:
        print_error(f"Error starting capture: {e}")
        return None


def simulate_dns_failure(interface: str, bad_dns: str):
    """Simulate DNS failure by setting invalid DNS server."""
    print_step(5, "Simulating DNS Failure")
    
    print(f"Setting DNS to invalid server: {bad_dns}")
    
    if platform.system() == "Windows":
        run_command(f'powershell.exe -Command "Set-DnsClientServerAddress -InterfaceAlias \"{interface}\" -ServerAddresses \"{bad_dns}\""')
        run_command("powershell.exe -Command \"Clear-DnsClientCache\"")
    else:
        run_command(f"sudo resolvectl dns {interface} {bad_dns}")
        run_command("sudo resolvectl flush-caches")
    
    time.sleep(2)
    print_success("DNS failure simulated")


def test_dns_failure(target_domain: str):
    """Test DNS resolution (should fail)."""
    print_step(6, "Testing DNS Resolution (Expected to Fail)")
    
    print(f"Testing ping to {target_domain}...")
    if platform.system() == "Windows":
        run_command(f"ping -n 3 {target_domain}")
        print(f"\nTesting DNS lookup with nslookup...")
        run_command(f"nslookup {target_domain}")
    else:
        run_command(f"ping -c 3 {target_domain}")
        print(f"\nTesting DNS lookup with dig...")
        run_command(f"dig {target_domain}")
    
    print_warning("DNS resolution should be failing now")


def restore_dns(interface: str, good_dns: str):
    """Restore DNS configuration."""
    print_step(7, "Restoring DNS Configuration")
    
    print(f"Setting DNS back to working server: {good_dns}")
    
    if platform.system() == "Windows":
        run_command(f'powershell.exe -Command "Set-DnsClientServerAddress -InterfaceAlias \"{interface}\" -ServerAddresses \"{good_dns}\""')
        run_command("powershell.exe -Command \"Clear-DnsClientCache\"")
    else:
        run_command(f"sudo resolvectl dns {interface} {good_dns}")
        run_command("sudo resolvectl flush-caches")
    
    time.sleep(2)
    print_success("DNS configuration restored")


def test_dns_recovery(target_domain: str):
    """Test DNS resolution (should work)."""
    print_step(8, "Testing DNS Resolution (Should Work Now)")
    
    print(f"Testing ping to {target_domain}...")
    if platform.system() == "Windows":
        run_command(f"ping -n 3 {target_domain}")
        print(f"\nTesting DNS lookup with nslookup...")
        run_command(f"nslookup {target_domain}")
    else:
        run_command(f"ping -c 3 {target_domain}")
        print(f"\nTesting DNS lookup with dig...")
        run_command(f"dig {target_domain}")
    
    print_success("DNS resolution should be working now")


def stop_wireshark_capture(pid: int, capture_file: str):
    """Stop Wireshark capture."""
    print_step(9, "Stopping Wireshark Capture")
    
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        
        # Check if process is still running
        try:
            os.kill(pid, 0)
            print_warning("Process still running, force killing...")
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        
        print_success("Wireshark capture stopped")
        print(f"Capture saved as: {capture_file}")
        print_warning("You can open this file in Wireshark to analyze DNS queries")
        
    except Exception as e:
        print_error(f"Error stopping capture: {e}")


def display_analysis_tips():
    """Display tips for analyzing the capture file."""
    print_step(10, "Analysis Tips")
    
    tips = [
        "Open the capture file in Wireshark",
        "Filter by 'dns' to see only DNS traffic",
        "Look for failed DNS queries (NXDOMAIN responses)",
        "Analyze the timing of DNS requests",
        "Check for DNS server timeouts",
        "Compare before/after DNS resolution behavior",
        "Use 'ip.addr == 123.123.123.123' to see failed queries"
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"{Colors.OKCYAN}{i}. {tip}{Colors.ENDC}")


def check_privileges():
    """Check if running with appropriate privileges."""
    if platform.system() == "Windows":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print_error("This script requires administrator privileges")
                print_warning("Please run as Administrator")
                print_warning("Right-click Command Prompt/PowerShell and select 'Run as administrator'")
                return False
        except:
            print_warning("Could not determine admin status")
    else:
        # Linux/Unix
        is_root = os.geteuid() == 0
        if not is_root:
            print_error("This script requires root privileges (sudo)")
            print_warning("Please run with: sudo python3 dns_resolve_interactive.py")
            return False
    
    return True


def main():
    """Main function for interactive DNS troubleshooting simulation."""
    print_header("Interactive DNS Troubleshooter Simulation Toolkit")
    print(f"{Colors.BOLD}This tool demonstrates DNS troubleshooting with Wireshark integration{Colors.ENDC}")
    print(f"{Colors.WARNING}Requires elevated privileges for network configuration{Colors.ENDC}")
    
    # Check privileges
    if not check_privileges():
        sys.exit(1)
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        sys.exit(1)
    
    # Get network interface
    interface = get_network_interface()
    if not interface:
        print_error("Could not determine network interface")
        sys.exit(1)
    
    # Configure simulation
    config = configure_simulation()
    
    # Configuration summary
    print_info("Configuration Summary:")
    print(f"  Interface: {interface}")
    print(f"  Target Domain: {config['target_domain']}")
    print(f"  Bad DNS: {config['bad_dns']}")
    print(f"  Good DNS: {config['good_dns']}")
    print(f"  Capture Duration: {config['capture_duration']} seconds")
    print(f"  Capture File: {config['capture_file']}")
    
    if not confirm_action("Start the DNS troubleshooting simulation?", True):
        print_info("Simulation cancelled by user")
        sys.exit(0)
    
    wireshark_pid = None
    
    try:
        # Display network info
        display_network_info(interface, config)
        
        # Start Wireshark capture
        wireshark_pid = start_wireshark_capture(interface, config['capture_file'])
        if not wireshark_pid:
            print_error("Failed to start capture, continuing without it...")
        
        # Simulate DNS failure
        simulate_dns_failure(interface, config['bad_dns'])
        
        # Test DNS failure
        test_dns_failure(config['target_domain'])
        
        # Wait for user to observe
        if confirm_action("Press Enter when ready to restore DNS", False):
            pass
        
        # Restore DNS
        restore_dns(interface, config['good_dns'])
        
        # Test DNS recovery
        test_dns_recovery(config['target_domain'])
        
        # Stop capture
        if wireshark_pid:
            stop_wireshark_capture(wireshark_pid, config['capture_file'])
        
        # Analysis tips
        display_analysis_tips()
        
        print_header("DNS Troubleshooting Simulation Complete")
        print_success("All steps completed successfully!")
        print(f"{Colors.BOLD}Capture file: {config['capture_file']}{Colors.ENDC}")
        
        if confirm_action("Open capture file in Wireshark now?", False):
            if platform.system() == "Windows":
                run_command(f'start wireshark "{config["capture_file"]}"')
            else:
                run_command(f"wireshark {config['capture_file']} &")
        
    except KeyboardInterrupt:
        print_warning("\nSimulation interrupted by user")
        if wireshark_pid:
            print("Stopping Wireshark capture...")
            stop_wireshark_capture(wireshark_pid, config['capture_file'])
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if wireshark_pid:
            stop_wireshark_capture(wireshark_pid, config['capture_file'])


if __name__ == "__main__":
    main()
