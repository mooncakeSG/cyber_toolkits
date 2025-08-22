import subprocess 
import os
import time
import socket
import platform
import psutil
import ctypes
from datetime import datetime 
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

LOG_FILE = f"dns_toolkit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_admin_privileges():
    """Check and handle administrator privileges"""
    if not is_admin():
        print(f"{Fore.RED}{Style.BRIGHT}⚠️  ADMINISTRATOR PRIVILEGES REQUIRED{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}This script needs administrator privileges to modify DNS settings.")
        print(f"{Fore.CYAN}Please run the script as Administrator:")
        print(f"{Fore.WHITE}1. Right-click on PowerShell/Command Prompt")
        print(f"2. Select 'Run as administrator'")
        print(f"3. Navigate to this directory")
        print(f"4. Run: python enhanced_windows_version.py{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Alternatively, you can run the script in presentation mode without admin rights.")
        response = input(f"{Fore.CYAN}Continue in presentation mode? (y/n): {Style.RESET_ALL}").lower().strip()
        if response in ['y', 'yes']:
            return "presentation"
        else:
            return "exit"
    return "admin"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
    print(message)

def log_system_overview():
    """Log system overview to the log file only (no console output)"""
    info = get_system_info()
    
    # Write directly to log file without console output
    with open(LOG_FILE, "a") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"SYSTEM OVERVIEW SUMMARY\n")
        f.write(f"{'='*60}\n")
        
        # OS Information
        f.write(f"\nOperating System:\n")
        f.write(f"  Name: {info['os']['name']}\n")
        f.write(f"  Version: {info['os']['version']}\n")
        f.write(f"  Release: {info['os']['release']}\n")
        f.write(f"  Architecture: {info['os']['architecture']}\n")
        
        # CPU Information
        f.write(f"\nProcessor:\n")
        f.write(f"  Name: {info['cpu']['name']}\n")
        f.write(f"  Cores: {info['cpu']['cores']}\n")
        f.write(f"  Threads: {info['cpu']['threads']}\n")
        f.write(f"  Current Usage: {info['cpu']['usage']:.1f}%\n")
        
        # Memory Information
        f.write(f"\nMemory:\n")
        f.write(f"  Total: {format_bytes(info['memory']['total'])}\n")
        f.write(f"  Available: {format_bytes(info['memory']['available'])}\n")
        f.write(f"  Used: {format_bytes(info['memory']['used'])} ({info['memory']['percent']:.1f}%)\n")
        
        # Storage Information
        f.write(f"\nStorage:\n")
        f.write(f"  Total: {format_bytes(info['storage']['total'])}\n")
        f.write(f"  Used: {format_bytes(info['storage']['used'])} ({info['storage']['percent']:.1f}%)\n")
        f.write(f"  Free: {format_bytes(info['storage']['free'])}\n")
        
        # Network Information
        f.write(f"\nNetwork:\n")
        f.write(f"  Hostname: {info['network']['hostname']}\n")
        f.write(f"  IP Address: {info['network']['ip']}\n")
        f.write(f"  Interfaces:\n")
        for interface, ip in info['network']['interfaces'].items():
            f.write(f"    {interface}: {ip}\n")
        
        f.write(f"\n{'='*60}\n")
    
    # Only show a brief message on console
    print(f"{Fore.GREEN}{Style.BRIGHT}✓ System overview logged to {LOG_FILE}{Style.RESET_ALL}")

def run_cmd(cmd, capture_output=False):
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
    if capture_output:
        return result 
    else:
        print(f"{Style.DIM}Executed: {cmd}{Style.RESET_ALL}")

def detect_interface():
    """Detect the primary network interface on Windows"""
    try:
        # Get detailed interface information to find the active one
        result = subprocess.run("ipconfig /all", shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        
        current_interface = None
        for line in lines:
            # Look for adapter headers
            if "Ethernet adapter" in line or "Wireless LAN adapter" in line:
                current_interface = line.split(":")[0].replace("Ethernet adapter", "").replace("Wireless LAN adapter", "").strip()
            
            # Look for IPv4 address that's not link-local (169.254.x.x)
            elif "IPv4 Address" in line and current_interface:
                ip_part = line.split(":")[1].strip() if ":" in line else ""
                # Extract IP address (remove Preferred suffix if present)
                ip = ip_part.split("(Preferred)")[0].strip() if "(Preferred)" in ip_part else ip_part
                
                # Check if it's a real IP (not link-local)
                if ip and not ip.startswith("169.254.") and ip != "127.0.0.1":
                    log(f"{Fore.YELLOW}{Style.BRIGHT}Using active interface: {current_interface} (IP: {ip}){Style.RESET_ALL}")
                    return current_interface
        
        # If no active interface found, try netsh method
        result = subprocess.run("netsh interface show interface", shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if "Enabled" in line and ("Ethernet" in line or "Wi-Fi" in line):
                parts = line.split()
                if len(parts) >= 4:
                    interface = parts[3]
                    log(f"{Fore.YELLOW}{Style.BRIGHT}Using enabled interface: {interface}{Style.RESET_ALL}")
                    return interface
    except:
        pass
    
    # Fallback: use ipconfig to get adapter names
    result = subprocess.run("ipconfig", shell=True, capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    for line in lines:
        if "Ethernet adapter" in line or "Wireless LAN adapter" in line:
            interface = line.split(":")[0].replace("Ethernet adapter", "").replace("Wireless LAN adapter", "").strip()
            log(f"{Fore.YELLOW}{Style.BRIGHT}Using fallback interface: {interface}{Style.RESET_ALL}")
            return interface
    
    # Ultimate fallback
    interface = "Wi-Fi"
    log(f"{Fore.YELLOW}{Style.BRIGHT}Using default interface: {interface}{Style.RESET_ALL}")
    return interface

def start_wireshark(interface):
    """Start Wireshark capture on Windows"""
    capture_file = f"dns_capture_{interface}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
    log(f"{Fore.GREEN}{Style.BRIGHT}Starting Wireshark capture on {interface}...{Style.RESET_ALL}")
    
    # Try to start Wireshark if available
    try:
        # Use interface index for Windows tshark
        process = subprocess.Popen(
            f'tshark -i "{interface}" -f "udp port 53" -w {capture_file}',
            shell=True
        )
        time.sleep(2)
        return process, capture_file
    except:
        # If tshark not available, create a dummy process
        log(f"{Fore.YELLOW}{Style.BRIGHT}Wireshark/tshark not available. Creating dummy capture file.{Style.RESET_ALL}")
        with open(capture_file, 'w') as f:
            f.write("DNS Capture Simulation - Wireshark not available\n")
        return None, capture_file

def stop_wireshark(process):
    if process:
        process.terminate()
        process.wait()
        log(f"{Fore.GREEN}{Style.BRIGHT}Wireshark capture stopped.{Style.RESET_ALL}")
    else:
        log(f"{Fore.GREEN}{Style.BRIGHT}Dummy capture completed.{Style.RESET_ALL}")

def open_pcap_in_wireshark(capture_file):
    """Open the captured .pcap file in Wireshark"""
    try:
        # Check if the capture file exists
        if os.path.exists(capture_file):
            print(f"{Fore.CYAN}{Style.BRIGHT}Opening capture file in Wireshark...{Style.RESET_ALL}")
            
            # Try to open with Wireshark
            subprocess.Popen(f'wireshark "{capture_file}"', shell=True)
            print(f"{Fore.GREEN}{Style.BRIGHT}✓ Capture file opened in Wireshark{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Tip: Use filter 'dns' to see only DNS traffic{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}{Style.BRIGHT}✗ Capture file not found: {capture_file}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}✗ Failed to open Wireshark: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}You can manually open the file: {capture_file}{Style.RESET_ALL}")
        return False

def get_dns_servers():
    """Get current DNS servers on Windows"""
    result = subprocess.run("ipconfig /all", shell=True, capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    dns_servers = []
    
    for line in lines:
        if "DNS Servers" in line and ":" in line:
            dns = line.split(":")[1].strip()
            if dns and dns != "":
                dns_servers.append(dns)
    
    return dns_servers

def set_dns_servers(interface, dns_servers):
    """Set DNS servers on Windows"""
    # Set primary DNS
    cmd = f'netsh interface ip set dns name="{interface}" static {dns_servers[0]}'
    run_cmd(cmd)
    
    # Set secondary DNS if provided
    if len(dns_servers) > 1:
        cmd = f'netsh interface ip add dns name="{interface}" {dns_servers[1]} index=2'
        run_cmd(cmd)

def flush_dns():
    """Flush DNS cache on Windows"""
    run_cmd("ipconfig /flushdns")

def verify_dns_failure():
    """Verify that DNS is actually broken"""
    print(f"{Fore.YELLOW}Verifying DNS failure...{Style.RESET_ALL}")
    result = subprocess.run("nslookup google.com", shell=True, capture_output=True, text=True)
    if "timed out" in result.stdout.lower() or "server failed" in result.stdout.lower():
        print(f"{Fore.GREEN}✓ DNS failure confirmed{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}✗ DNS still working - failure simulation may not be complete{Style.RESET_ALL}")
        return False

def simulate_dns_failure():
    """Simulate DNS failure without actually changing system settings"""
    print(f"{Fore.YELLOW}PRESENTATION MODE: DNS failure would be simulated here{Style.RESET_ALL}")
    print(f"{Fore.CYAN}In a real scenario, this would:")
    print(f"  - Change DNS servers to invalid addresses")
    print(f"  - Cause DNS resolution to fail")
    print(f"  - Demonstrate troubleshooting steps{Style.RESET_ALL}")
    time.sleep(2)
    return True

def simulate_dns_restore():
    """Simulate DNS restoration without actually changing system settings"""
    print(f"{Fore.YELLOW}PRESENTATION MODE: DNS restoration would be simulated here{Style.RESET_ALL}")
    print(f"{Fore.CYAN}In a real scenario, this would:")
    print(f"  - Restore DNS servers to working addresses")
    print(f"  - Flush DNS cache")
    print(f"  - Verify DNS resolution is working{Style.RESET_ALL}")
    time.sleep(2)
    return True

def check_wireshark_installed():
    """Check if Wireshark/tshark is installed on Windows"""
    try:
        result = subprocess.run("tshark --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except:
        pass
    
    # Also check for Wireshark in common installation paths
    common_paths = [
        r"C:\Program Files\Wireshark\tshark.exe",
        r"C:\Program Files (x86)\Wireshark\tshark.exe",
        r"C:\Wireshark\tshark.exe"
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            # Add to PATH temporarily
            os.environ['PATH'] = os.path.dirname(path) + os.pathsep + os.environ.get('PATH', '')
            return True
    
    return False

def install_wireshark_windows():
    """Install Wireshark on Windows using package managers"""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Wireshark not found. Attempting to install...{Style.RESET_ALL}")
    
    # Try winget first (Windows 10/11)
    try:
        print(f"{Fore.CYAN}Attempting to install Wireshark using winget...{Style.RESET_ALL}")
        result = subprocess.run("winget install WiresharkFoundation.Wireshark", shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{Fore.GREEN}✓ Wireshark installation initiated successfully!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please complete the installation manually and restart the script.{Style.RESET_ALL}")
            return False  # Return False so script stops and user can restart
    except:
        pass
    
    # Try chocolatey if available
    try:
        print(f"{Fore.CYAN}Attempting to install Wireshark using Chocolatey...{Style.RESET_ALL}")
        result = subprocess.run("choco install wireshark -y", shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{Fore.GREEN}✓ Wireshark installed successfully via Chocolatey!{Style.RESET_ALL}")
            return True
    except:
        pass
    
    # Try scoop if available
    try:
        print(f"{Fore.CYAN}Attempting to install Wireshark using Scoop...{Style.RESET_ALL}")
        result = subprocess.run("scoop install wireshark", shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{Fore.GREEN}✓ Wireshark installed successfully via Scoop!{Style.RESET_ALL}")
            return True
    except:
        pass
    
    # Fallback: Manual download instructions
    print(f"{Fore.RED}✗ Automatic installation failed.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Please install Wireshark manually:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}1. Visit: https://www.wireshark.org/download.html")
    print(f"2. Download the Windows installer")
    print(f"3. Run the installer and follow the prompts")
    print(f"4. Restart this script after installation{Style.RESET_ALL}")
    
    # Try to open the download page
    try:
        subprocess.run("start https://www.wireshark.org/download.html", shell=True)
    except:
        pass
    
    return False

def ensure_wireshark_available():
    """Ensure Wireshark is available, install if necessary"""
    if check_wireshark_installed():
        print(f"{Fore.GREEN}{Style.BRIGHT}✓ Wireshark/tshark is already installed{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.YELLOW}{Style.BRIGHT}✗ Wireshark/tshark not found{Style.RESET_ALL}")
        install_success = install_wireshark_windows()
        
        # If installation was successful, re-check if Wireshark is now available
        if install_success:
            print(f"{Fore.CYAN}Re-checking Wireshark installation...{Style.RESET_ALL}")
            if check_wireshark_installed():
                print(f"{Fore.GREEN}{Style.BRIGHT}✓ Wireshark/tshark is now available!{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.YELLOW}Wireshark installation may need a system restart.{Style.RESET_ALL}")
                return False
        
        return False

def get_system_info():
    """Get comprehensive system information"""
    info = {}
    
    # OS Information
    info['os'] = {
        'name': platform.system(),
        'version': platform.version(),
        'release': platform.release(),
        'architecture': platform.architecture()[0],
        'machine': platform.machine()
    }
    
    # CPU Information
    info['cpu'] = {
        'name': platform.processor(),
        'cores': psutil.cpu_count(logical=False),
        'threads': psutil.cpu_count(logical=True),
        'usage': psutil.cpu_percent(interval=1)
    }
    
    # Memory Information
    memory = psutil.virtual_memory()
    info['memory'] = {
        'total': memory.total,
        'available': memory.available,
        'used': memory.used,
        'percent': memory.percent
    }
    
    # Storage Information
    disk = psutil.disk_usage('/')
    info['storage'] = {
        'total': disk.total,
        'used': disk.used,
        'free': disk.free,
        'percent': (disk.used / disk.total) * 100
    }
    
    # Network Information
    info['network'] = {}
    try:
        # Get hostname
        info['network']['hostname'] = socket.gethostname()
        
        # Get IP address
        info['network']['ip'] = socket.gethostbyname(socket.gethostname())
        
        # Get network interfaces
        interfaces = psutil.net_if_addrs()
        info['network']['interfaces'] = {}
        for interface, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4
                    info['network']['interfaces'][interface] = addr.address
                    break
    except:
        info['network']['hostname'] = "Unknown"
        info['network']['ip'] = "Unknown"
        info['network']['interfaces'] = {}
    
    return info

def format_bytes(bytes_value):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def display_system_info():
    """Display system information in a clean format"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*60}")
    print(f"{Fore.CYAN}{Style.BRIGHT}SYSTEM INFORMATION")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'='*60}{Style.RESET_ALL}")
    
    info = get_system_info()
    
    # OS Information
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Operating System:{Style.RESET_ALL}")
    print(f"  Name: {info['os']['name']}")
    print(f"  Version: {info['os']['version']}")
    print(f"  Release: {info['os']['release']}")
    print(f"  Architecture: {info['os']['architecture']}")
    
    # CPU Information
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Processor:{Style.RESET_ALL}")
    print(f"  Name: {info['cpu']['name']}")
    print(f"  Cores: {info['cpu']['cores']}")
    print(f"  Threads: {info['cpu']['threads']}")
    print(f"  Current Usage: {info['cpu']['usage']:.1f}%")
    
    # Memory Information
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Memory:{Style.RESET_ALL}")
    print(f"  Total: {format_bytes(info['memory']['total'])}")
    print(f"  Available: {format_bytes(info['memory']['available'])}")
    print(f"  Used: {format_bytes(info['memory']['used'])} ({info['memory']['percent']:.1f}%)")
    
    # Storage Information
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Storage:{Style.RESET_ALL}")
    print(f"  Total: {format_bytes(info['storage']['total'])}")
    print(f"  Used: {format_bytes(info['storage']['used'])} ({info['storage']['percent']:.1f}%)")
    print(f"  Free: {format_bytes(info['storage']['free'])}")
    
    # Network Information
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Network:{Style.RESET_ALL}")
    print(f"  Hostname: {info['network']['hostname']}")
    print(f"  IP Address: {info['network']['ip']}")
    print(f"  Interfaces:")
    for interface, ip in info['network']['interfaces'].items():
        print(f"    {interface}: {ip}")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*60}{Style.RESET_ALL}")

def main():
    print(f"\n{Fore.RED}{Style.BRIGHT}Windows DNS Troubleshooter Simulation Toolkit{Style.RESET_ALL}")
    
    # Check administrator privileges first
    admin_status = check_admin_privileges()
    if admin_status == "exit":
        return
    elif admin_status == "presentation":
        print(f"{Fore.YELLOW}{Style.BRIGHT}Running in PRESENTATION MODE{Style.RESET_ALL}")
        presentation_mode = True
    else:
        print(f"{Fore.GREEN}{Style.BRIGHT}Running with Administrator privileges{Style.RESET_ALL}")
        presentation_mode = False
    
    # Display system information first
    display_system_info()
    
    # Check and ensure Wireshark is available
    print(f"\n{Fore.BLUE}{Style.BRIGHT}=== Checking Wireshark Availability ==={Style.RESET_ALL}")
    if not ensure_wireshark_available():
        print(f"{Fore.RED}{Style.BRIGHT}Wireshark installation required.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}You can continue without Wireshark (packet capture will be simulated), or install Wireshark and restart.{Style.RESET_ALL}")
        
        # Ask user if they want to continue without Wireshark
        try:
            response = input(f"{Fore.CYAN}Continue without Wireshark? (y/n): {Style.RESET_ALL}").lower().strip()
            if response not in ['y', 'yes']:
                print(f"{Fore.YELLOW}Please install Wireshark and restart the script.{Style.RESET_ALL}")
                return
            else:
                print(f"{Fore.YELLOW}Continuing without Wireshark - packet capture will be simulated.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Script interrupted by user.{Style.RESET_ALL}")
            return
    
    interface = detect_interface()

    # --- Step 1: Display current network info ---
    print(f"\n{Fore.BLUE}{Style.BRIGHT}=== Current Network Info ==={Style.RESET_ALL}")
    run_cmd(f"ipconfig /all")
    
    # Get current DNS servers
    current_dns = get_dns_servers()
    log(f"{Fore.CYAN}{Style.BRIGHT}Current DNS servers: {current_dns}{Style.RESET_ALL}")

    # Step 2: Start Wireshark
    ws_process, capture_file = start_wireshark(interface)

    # Step 3: Simulate DNS failure
    print(f"\n{Fore.RED}{Style.BRIGHT}Step 2: Simulating DNS Failure{Style.RESET_ALL}")
    
    if presentation_mode:
        simulate_dns_failure()
    else:
        # Use a completely invalid DNS server to ensure failure
        set_dns_servers(interface, ["0.0.0.0"])
        time.sleep(3)  # Give more time for DNS changes to take effect
        
        # Verify DNS is actually broken
        verify_dns_failure()

    # Step 4: Test DNS failure
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Step 3: Testing DNS Resolution (Should Fail){Style.RESET_ALL}")
    run_cmd("ping -n 3 google.com")
    run_cmd("nslookup google.com")

    # Step 5: Test IP connectivity
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Step 4: Testing IP Connectivity (Should Succeed){Style.RESET_ALL}")
    run_cmd("ping -n 3 8.8.8.8")

    # Step 6: Restore DNS
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Step 5: Restoring DNS{Style.RESET_ALL}")
    
    if presentation_mode:
        simulate_dns_restore()
    else:
        set_dns_servers(interface, ["8.8.8.8", "8.8.4.4"])
        flush_dns()
        time.sleep(2)

    # Step 7: Verify DNS
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Step 6: Verifying DNS Resolution{Style.RESET_ALL}")
    run_cmd("ping -n 3 google.com")
    run_cmd("nslookup google.com")

    # Stop Wireshark
    stop_wireshark(ws_process)
    log(f"{Fore.GREEN}{Style.BRIGHT}Capture saved as {capture_file}{Style.RESET_ALL}")

    # Open the capture file in Wireshark
    open_pcap_in_wireshark(capture_file)

    # Log system overview at the end
    log_system_overview()

    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== Simulation Complete. Log saved to {LOG_FILE} ==={Style.RESET_ALL}")

if __name__ == "__main__":
    main()
