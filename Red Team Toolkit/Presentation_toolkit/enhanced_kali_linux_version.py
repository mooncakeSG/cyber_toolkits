import subprocess 
import os
import time
import platform
import psutil
from datetime import datetime 
from rich import print 
from rich.console import Console 
from rich.progress import track 

console = Console()
LOG_FILE = f"dns_toolkit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
    console.print(message)

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
    console.print(f"[bold green]✓ System overview logged to {LOG_FILE}[/bold green]")

def run_cmd(cmd, capture_output=False):
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
    if capture_output:
        return result 
    
def detect_interface():
    """Detect the primary network interface on Linux"""
    try:
        # Get the default route interface
        result = subprocess.run("ip route | grep '^default' | awk '{print $5}'", shell=True, capture_output=True, text=True)
        interface = result.stdout.strip()
        
        if interface:
            # Verify the interface is up and has an IP
            result = subprocess.run(f"ip addr show {interface}", shell=True, capture_output=True, text=True)
            if "UP" in result.stdout and "inet " in result.stdout:
                log(f"[bold yellow]Using active interface: {interface}[/bold yellow]")
                return interface
        
        # Fallback: find any interface with an IP
        result = subprocess.run("ip addr show | grep -E '^[0-9]+:' | awk '{print $2}' | sed 's/://'", shell=True, capture_output=True, text=True)
        interfaces = result.stdout.strip().split('\n')
        
        for iface in interfaces:
            if iface and iface != "lo":  # Skip loopback
                result = subprocess.run(f"ip addr show {iface}", shell=True, capture_output=True, text=True)
                if "UP" in result.stdout and "inet " in result.stdout:
                    log(f"[bold yellow]Using fallback interface: {iface}[/bold yellow]")
                    return iface
    except:
        pass
    
    # Ultimate fallback
    interface = "eth0"
    log(f"[bold yellow]Using default interface: {interface}[/bold yellow]")
    return interface 

def start_wireshark(interface):
    capture_file = f"dns_capture_{interface}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
    log(f"[bold green]Starting Wireshark capture on {interface}...[/bold green]")
    process = subprocess.Popen(
        f"sudo tshark -i {interface} -f 'udp port 53' -w {capture_file}",
        shell=True
        
    ) 
    time.sleep(2)
    return process, capture_file 

def stop_wireshark(process):
    process.terminate()
    process.wait()
    log(f"[bold green]Wireshark capture stopped.[/bold green]")

def open_pcap_in_wireshark(capture_file):
    """Open the captured .pcap file in Wireshark"""
    try:
        # Check if the capture file exists
        if os.path.exists(capture_file):
            console.print(f"[cyan]Opening capture file in Wireshark...[/cyan]")
            
            # Try to open with Wireshark
            subprocess.Popen(f'wireshark "{capture_file}"', shell=True)
            console.print(f"[bold green]✓ Capture file opened in Wireshark[/bold green]")
            console.print(f"[yellow]Tip: Use filter 'dns' to see only DNS traffic[/yellow]")
            return True
        else:
            console.print(f"[bold red]✗ Capture file not found: {capture_file}[/bold red]")
            return False
    except Exception as e:
        console.print(f"[bold red]✗ Failed to open Wireshark: {e}[/bold red]")
        console.print(f"[yellow]You can manually open the file: {capture_file}[/yellow]")
        return False

def check_wireshark_installed():
    """Check if Wireshark/tshark is installed on Linux"""
    try:
        result = subprocess.run("tshark --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except:
        pass
    
    # Also check for tshark in common paths
    common_paths = [
        "/usr/bin/tshark",
        "/usr/local/bin/tshark",
        "/opt/wireshark/bin/tshark"
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return True
    
    return False

def install_wireshark_linux():
    """Install Wireshark on Linux using package managers"""
    console.print(f"\n[bold yellow]Wireshark not found. Attempting to install...[/bold yellow]")
    
    # Detect package manager and install
    package_managers = [
        ("apt", "apt-get install -y wireshark-qt"),
        ("yum", "yum install -y wireshark"),
        ("dnf", "dnf install -y wireshark"),
        ("pacman", "pacman -S --noconfirm wireshark-qt"),
        ("zypper", "zypper install -y wireshark"),
        ("emerge", "emerge wireshark")
    ]
    
    for pkg_mgr, install_cmd in package_managers:
        try:
            # Check if package manager exists
            result = subprocess.run(f"which {pkg_mgr}", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                console.print(f"[cyan]Attempting to install Wireshark using {pkg_mgr}...[/cyan]")
                
                # Update package list first
                if pkg_mgr in ["apt", "apt-get"]:
                    subprocess.run("sudo apt-get update", shell=True, capture_output=True, text=True)
                elif pkg_mgr in ["yum", "dnf"]:
                    subprocess.run(f"sudo {pkg_mgr} update", shell=True, capture_output=True, text=True)
                
                # Install Wireshark
                result = subprocess.run(f"sudo {install_cmd}", shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    console.print(f"[bold green]✓ Wireshark installed successfully via {pkg_mgr}![/bold green]")
                    return True
                else:
                    console.print(f"[red]✗ Installation via {pkg_mgr} failed.[/red]")
        except:
            continue
    
    # Fallback: Manual installation instructions
    console.print(f"[bold red]✗ Automatic installation failed.[/bold red]")
    console.print(f"[yellow]Please install Wireshark manually:[/yellow]")
    console.print(f"[cyan]For Debian/Ubuntu/Kali: sudo apt-get install wireshark-qt")
    console.print(f"For CentOS/RHEL: sudo yum install wireshark")
    console.print(f"For Arch: sudo pacman -S wireshark-qt")
    console.print(f"For openSUSE: sudo zypper install wireshark")
    console.print(f"Or visit: https://www.wireshark.org/download.html[/cyan]")
    
    return False

def ensure_wireshark_available():
    """Ensure Wireshark is available, install if necessary"""
    if check_wireshark_installed():
        console.print(f"[bold green]✓ Wireshark/tshark is already installed[/bold green]")
        return True
    else:
        console.print(f"[bold yellow]✗ Wireshark/tshark not found[/bold yellow]")
        return install_wireshark_linux()

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
        info['network']['hostname'] = platform.node()
        
        # Get IP address
        import socket
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
    console.print(f"\n[bold cyan]{'='*60}")
    console.print(f"[bold cyan]SYSTEM INFORMATION")
    console.print(f"[bold cyan]{'='*60}")
    
    info = get_system_info()
    
    # OS Information
    console.print(f"\n[bold yellow]Operating System:")
    console.print(f"  Name: {info['os']['name']}")
    console.print(f"  Version: {info['os']['version']}")
    console.print(f"  Release: {info['os']['release']}")
    console.print(f"  Architecture: {info['os']['architecture']}")
    
    # CPU Information
    console.print(f"\n[bold yellow]Processor:")
    console.print(f"  Name: {info['cpu']['name']}")
    console.print(f"  Cores: {info['cpu']['cores']}")
    console.print(f"  Threads: {info['cpu']['threads']}")
    console.print(f"  Current Usage: {info['cpu']['usage']:.1f}%")
    
    # Memory Information
    console.print(f"\n[bold yellow]Memory:")
    console.print(f"  Total: {format_bytes(info['memory']['total'])}")
    console.print(f"  Available: {format_bytes(info['memory']['available'])}")
    console.print(f"  Used: {format_bytes(info['memory']['used'])} ({info['memory']['percent']:.1f}%)")
    
    # Storage Information
    console.print(f"\n[bold yellow]Storage:")
    console.print(f"  Total: {format_bytes(info['storage']['total'])}")
    console.print(f"  Used: {format_bytes(info['storage']['used'])} ({info['storage']['percent']:.1f}%)")
    console.print(f"  Free: {format_bytes(info['storage']['free'])}")
    
    # Network Information
    console.print(f"\n[bold yellow]Network:")
    console.print(f"  Hostname: {info['network']['hostname']}")
    console.print(f"  IP Address: {info['network']['ip']}")
    console.print(f"  Interfaces:")
    for interface, ip in info['network']['interfaces'].items():
        console.print(f"    {interface}: {ip}")
    
    console.print(f"\n[bold cyan]{'='*60}")

def main():
    console.print("\n[bold red]Kali DNS Troubleshooter Simulation Toolkit[/bold red]")
    
    # Display system information first
    display_system_info()
    
    # Check and ensure Wireshark is available
    console.print(f"\n[bold blue]=== Checking Wireshark Availability ===[/bold blue]")
    if not ensure_wireshark_available():
        console.print(f"[bold red]Wireshark installation required.[/bold red]")
        console.print(f"[yellow]You can continue without Wireshark (packet capture will be simulated), or install Wireshark and restart.[/yellow]")
        
        # Ask user if they want to continue without Wireshark
        try:
            response = input("Continue without Wireshark? (y/n): ").lower().strip()
            if response not in ['y', 'yes']:
                console.print(f"[yellow]Please install Wireshark and restart the script.[/yellow]")
                return
            else:
                console.print(f"[yellow]Continuing without Wireshark - packet capture will be simulated.[/yellow]")
        except KeyboardInterrupt:
            console.print(f"\n[yellow]Script interrupted by user.[/yellow]")
            return
    
    interface = detect_interface()

    # --- Step 1: Display current network info ---
    console.print("\n[bold blue]=== Current Network Info ===[/bold blue]")
    run_cmd(f"ip a show {interface}")
    run_cmd(f"cat /etc/resolv.conf")

    # Step 2: Start Wireshark
    ws_process, capture_file = start_wireshark(interface)

    # Step 3: Simulate DNS failure
    console.print("\n[bold red]Step 2: Simulating DNS Failure[/bold red]")
    run_cmd(f"sudo resolvectl dns {interface} 123.123.123.123")
    time.sleep(2)

    # Step 4: Test DNS failure
    console.print("\n[bold yellow]Step 3: Testing DNS Resolution (Should Fail)[/bold yellow]")
    run_cmd("ping -c 3 google.com")
    run_cmd("dig google.com")

    # Step 5: Test IP connectivity
    console.print("\n[bold magenta]Step 4: Testing IP Connectivity (Should Succeed)[/bold magenta]")
    run_cmd("ping -c 3 8.8.8.8")

    # Step 6: Resolve DNS
    console.print("\n[bold green]Step 5: Restoring DNS[/bold green]")
    run_cmd(f"sudo resolvectl dns {interface} 8.8.8.8")
    run_cmd("sudo resolvectl flush-caches")
    time.sleep(2)

    # Step 7: Verify DNS
    console.print("\n[bold cyan]Step 6: Verifying DNS Resolution[/bold cyan]")
    run_cmd("ping -c 3 google.com")
    run_cmd("dig google.com")

    # Stop Wireshark
    stop_wireshark(ws_process)
    log(f"[bold green]Capture saved as {capture_file}[/bold green]")

    # Open the capture file in Wireshark
    open_pcap_in_wireshark(capture_file)

    # Log system overview at the end
    log_system_overview()

    console.print(f"\n[bold cyan]=== Simulation Complete. Log saved to {LOG_FILE} ===[/bold cyan]")

if __name__ == "__main__":
    main()
