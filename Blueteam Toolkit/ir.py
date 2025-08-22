"""
Incident Response module for the Blue Team CLI Toolkit.
Generates snapshot reports and provides quarantine functionality.
"""

import os
import sys
import platform
import subprocess
import shutil
import psutil
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import utils


def collect_process_information() -> List[Dict]:
    """Collect detailed process information."""
    processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'ppid', 'create_time', 'memory_info', 'cpu_percent', 'status', 'exe', 'cmdline']):
            try:
                proc_info = proc.info
                
                # Add additional information
                proc_info['memory_mb'] = round(proc_info['memory_info'].rss / 1024 / 1024, 2) if proc_info['memory_info'] else 0
                proc_info['cpu_percent'] = round(proc_info['cpu_percent'], 2) if proc_info['cpu_percent'] else 0
                proc_info['start_time'] = utils.format_timestamp(proc_info['create_time']) if proc_info['create_time'] else 'Unknown'
                proc_info['is_suspicious'] = utils.is_suspicious_process(proc_info['name'])
                
                # Calculate hash if executable path exists
                if proc_info['exe'] and os.path.exists(proc_info['exe']):
                    proc_info['file_hash'] = utils.calculate_hash(proc_info['exe'])
                else:
                    proc_info['file_hash'] = None
                
                processes.append(proc_info)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
    except Exception as e:
        utils.print_error(f"Error collecting process information: {e}")
    
    return processes


def collect_network_information() -> List[Dict]:
    """Collect network connection information."""
    connections = []
    
    try:
        for conn in psutil.net_connections():
            try:
                conn_info = {
                    'fd': conn.fd,
                    'family': str(conn.family),
                    'type': str(conn.type),
                    'laddr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                    'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                    'status': conn.status,
                    'pid': conn.pid
                }
                
                # Get process name for the connection
                if conn.pid:
                    try:
                        proc = psutil.Process(conn.pid)
                        conn_info['process_name'] = proc.name()
                        conn_info['process_exe'] = proc.exe()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        conn_info['process_name'] = 'Unknown'
                        conn_info['process_exe'] = 'Unknown'
                else:
                    conn_info['process_name'] = 'Unknown'
                    conn_info['process_exe'] = 'Unknown'
                
                connections.append(conn_info)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
    except Exception as e:
        utils.print_error(f"Error collecting network information: {e}")
    
    return connections


def collect_file_information() -> List[Dict]:
    """Collect information about recently modified files."""
    files = []
    
    try:
        # Common directories to check
        directories = []
        if platform.system() == "Windows":
            directories = [
                os.path.expanduser("~\\Desktop"),
                os.path.expanduser("~\\Documents"),
                os.path.expanduser("~\\Downloads"),
                "C:\\Temp",
                "C:\\Windows\\Temp"
            ]
        else:
            directories = [
                os.path.expanduser("~/Desktop"),
                os.path.expanduser("~/Documents"),
                os.path.expanduser("~/Downloads"),
                "/tmp",
                "/var/tmp"
            ]
        
        for directory in directories:
            if os.path.exists(directory):
                try:
                    for root, dirs, filenames in os.walk(directory):
                        for filename in filenames:
                            file_path = os.path.join(root, filename)
                            try:
                                stat = os.stat(file_path)
                                
                                # Only include files modified in the last 24 hours
                                if (datetime.now().timestamp() - stat.st_mtime) < 86400:
                                    file_info = {
                                        'path': file_path,
                                        'name': filename,
                                        'size': stat.st_size,
                                        'size_formatted': utils.format_bytes(stat.st_size),
                                        'modified_time': utils.format_timestamp(stat.st_mtime),
                                        'created_time': utils.format_timestamp(stat.st_ctime),
                                        'permissions': oct(stat.st_mode)[-3:],
                                        'hash': utils.calculate_hash(file_path) if stat.st_size < 100 * 1024 * 1024 else None  # Skip large files
                                    }
                                    files.append(file_info)
                            except (OSError, PermissionError):
                                continue
                except (OSError, PermissionError):
                    continue
                    
    except Exception as e:
        utils.print_error(f"Error collecting file information: {e}")
    
    return files


def collect_user_information() -> List[Dict]:
    """Collect user and session information."""
    users = []
    
    try:
        if platform.system() == "Windows":
            # Windows user information
            try:
                result = subprocess.run(
                    ["wmic", "useraccount", "get", "name,disabled,lockout", "/format:csv"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines[1:]:  # Skip header
                        if line.strip():
                            parts = line.split(',')
                            if len(parts) >= 3:
                                users.append({
                                    'name': parts[1],
                                    'disabled': parts[2] == 'TRUE',
                                    'lockout': parts[3] == 'TRUE' if len(parts) > 3 else False,
                                    'os': 'Windows'
                                })
            except Exception as e:
                utils.print_warning(f"Could not collect Windows user information: {e}")
                
        else:
            # Linux user information
            try:
                with open('/etc/passwd', 'r') as f:
                    for line in f:
                        parts = line.strip().split(':')
                        if len(parts) >= 7:
                            users.append({
                                'name': parts[0],
                                'uid': parts[2],
                                'gid': parts[3],
                                'home': parts[5],
                                'shell': parts[6],
                                'os': 'Linux'
                            })
            except Exception as e:
                utils.print_warning(f"Could not collect Linux user information: {e}")
                
    except Exception as e:
        utils.print_error(f"Error collecting user information: {e}")
    
    return users


def collect_system_information() -> Dict[str, Any]:
    """Collect comprehensive system information."""
    system_info = utils.get_system_info()
    
    # Add additional system information
    try:
        system_info.update({
            'boot_time': utils.format_timestamp(psutil.boot_time()),
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_total': utils.format_bytes(psutil.virtual_memory().total),
            'memory_available': utils.format_bytes(psutil.virtual_memory().available),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': {}
        })
        
        # Disk usage information
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                system_info['disk_usage'][partition.mountpoint] = {
                    'total': utils.format_bytes(usage.total),
                    'used': utils.format_bytes(usage.used),
                    'free': utils.format_bytes(usage.free),
                    'percent': usage.percent
                }
            except (OSError, PermissionError):
                continue
                
    except Exception as e:
        utils.print_error(f"Error collecting system information: {e}")
    
    return system_info


def quarantine_file(file_path: str) -> bool:
    """Quarantine a suspicious file."""
    try:
        if not os.path.exists(file_path):
            utils.print_error(f"File not found: {file_path}")
            return False
        
        # Create quarantine directory
        quarantine_dir = os.path.join(os.getcwd(), "quarantine")
        os.makedirs(quarantine_dir, exist_ok=True)
        
        # Generate quarantine filename
        filename = os.path.basename(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        quarantine_name = f"{timestamp}_{filename}"
        quarantine_path = os.path.join(quarantine_dir, quarantine_name)
        
        # Move file to quarantine
        shutil.move(file_path, quarantine_path)
        
        # Create quarantine log entry
        log_entry = {
            'original_path': file_path,
            'quarantine_path': quarantine_path,
            'quarantine_time': datetime.now().isoformat(),
            'file_hash': utils.calculate_hash(quarantine_path),
            'file_size': os.path.getsize(quarantine_path)
        }
        
        # Save quarantine log
        quarantine_log = os.path.join(quarantine_dir, "quarantine_log.json")
        try:
            import json
            if os.path.exists(quarantine_log):
                with open(quarantine_log, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = []
            
            log_data.append(log_entry)
            
            with open(quarantine_log, 'w') as f:
                json.dump(log_data, f, indent=2, default=str)
                
        except Exception as e:
            utils.print_warning(f"Could not update quarantine log: {e}")
        
        utils.print_success(f"File quarantined: {file_path} -> {quarantine_path}")
        return True
        
    except Exception as e:
        utils.print_error(f"Error quarantining file {file_path}: {e}")
        return False


def generate_ir_report(processes: List[Dict], connections: List[Dict], 
                      files: List[Dict], users: List[Dict], 
                      system_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a comprehensive incident response report."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'system_info': system_info,
        'summary': {
            'total_processes': len(processes),
            'suspicious_processes': len([p for p in processes if p.get('is_suspicious', False)]),
            'total_connections': len(connections),
            'established_connections': len([c for c in connections if c.get('status') == 'ESTABLISHED']),
            'recent_files': len(files),
            'total_users': len(users)
        },
        'processes': processes,
        'connections': connections,
        'files': files,
        'users': users,
        'analysis': {
            'suspicious_processes': [p for p in processes if p.get('is_suspicious', False)],
            'high_memory_processes': [p for p in processes if p.get('memory_mb', 0) > 500],
            'high_cpu_processes': [p for p in processes if p.get('cpu_percent', 0) > 50],
            'suspicious_connections': [c for c in connections if c.get('process_name') in ['cmd.exe', 'powershell.exe', 'wscript.exe']]
        }
    }
    
    return report


def display_ir_report(report: Dict[str, Any]):
    """Display the incident response report."""
    utils.print_section("Incident Response Report")
    
    # System Information
    print(f"Report Generated: {report['timestamp']}")
    print(f"Hostname: {report['system_info']['hostname']}")
    print(f"Platform: {report['system_info']['platform']}")
    print(f"Boot Time: {report['system_info'].get('boot_time', 'Unknown')}")
    print(f"CPU Usage: {report['system_info'].get('cpu_percent', 0)}%")
    print(f"Memory Usage: {report['system_info'].get('memory_percent', 0)}%")
    
    # Summary
    utils.print_section("Summary")
    summary = report['summary']
    print(f"Total Processes: {summary['total_processes']}")
    print(f"Suspicious Processes: {summary['suspicious_processes']}")
    print(f"Total Network Connections: {summary['total_connections']}")
    print(f"Established Connections: {summary['established_connections']}")
    print(f"Recent Files: {summary['recent_files']}")
    print(f"Total Users: {summary['total_users']}")
    
    # Suspicious Processes
    if report['analysis']['suspicious_processes']:
        utils.print_section("Suspicious Processes")
        for i, proc in enumerate(report['analysis']['suspicious_processes'][:10], 1):
            print(f"\n{i}. {proc['name']} (PID: {proc['pid']})")
            print(f"   Start Time: {proc['start_time']}")
            print(f"   Memory: {proc['memory_mb']} MB")
            print(f"   CPU: {proc['cpu_percent']}%")
            if proc.get('exe'):
                print(f"   Path: {proc['exe']}")
    
    # High Memory Processes
    if report['analysis']['high_memory_processes']:
        utils.print_section("High Memory Processes (>500MB)")
        for i, proc in enumerate(report['analysis']['high_memory_processes'][:5], 1):
            print(f"\n{i}. {proc['name']} (PID: {proc['pid']})")
            print(f"   Memory: {proc['memory_mb']} MB")
            print(f"   CPU: {proc['cpu_percent']}%")
    
    # Suspicious Network Connections
    if report['analysis']['suspicious_connections']:
        utils.print_section("Suspicious Network Connections")
        for i, conn in enumerate(report['analysis']['suspicious_connections'][:10], 1):
            print(f"\n{i}. Process: {conn['process_name']} (PID: {conn['pid']})")
            print(f"   Local: {conn['laddr']}")
            print(f"   Remote: {conn['raddr']}")
            print(f"   Status: {conn['status']}")


def block_ip_address(ip_address: str, duration: int = 3600) -> bool:
    """
    Block an IP address using system firewall.
    
    Args:
        ip_address: IP address to block
        duration: Block duration in seconds (default: 1 hour)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not utils.validate_ip(ip_address):
            utils.print_error(f"Invalid IP address: {ip_address}")
            return False
        
        if platform.system() == "Windows":
            # Windows firewall blocking
            rule_name = f"BlueTeam_Block_{ip_address.replace('.', '_')}"
            
            # Create firewall rule
            cmd = [
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name="{rule_name}"',
                'dir=out',
                'action=block',
                f'remoteip={ip_address}',
                'enable=yes'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                utils.print_success(f"IP {ip_address} blocked via Windows Firewall")
                
                # Schedule rule removal
                if duration > 0:
                    remove_cmd = [
                        'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                        f'name="{rule_name}"'
                    ]
                    
                    # Use schtasks to schedule rule removal
                    schedule_cmd = [
                        'schtasks', '/create', '/tn', f'RemoveBlock_{rule_name}',
                        '/tr', f'"{remove_cmd[0]}" {" ".join(remove_cmd[1:])}',
                        '/sc', 'once', '/st', 
                        (datetime.now() + timedelta(seconds=duration)).strftime('%H:%M'),
                        '/sd', datetime.now().strftime('%m/%d/%Y')
                    ]
                    
                    subprocess.run(schedule_cmd, capture_output=True, timeout=30)
                    utils.print_info(f"Block will be removed in {duration} seconds")
                
                return True
            else:
                utils.print_error(f"Failed to block IP {ip_address}: {result.stderr}")
                return False
                
        else:
            # Linux iptables blocking
            rule_name = f"BlueTeam_Block_{ip_address.replace('.', '_')}"
            
            # Add iptables rule
            cmd = ['iptables', '-A', 'OUTPUT', '-d', ip_address, '-j', 'DROP']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                utils.print_success(f"IP {ip_address} blocked via iptables")
                
                # Schedule rule removal
                if duration > 0:
                    remove_cmd = ['iptables', '-D', 'OUTPUT', '-d', ip_address, '-j', 'DROP']
                    
                    # Use at command to schedule removal
                    at_cmd = f'echo "{remove_cmd[0]} {" ".join(remove_cmd[1:])}" | at now + {duration} seconds'
                    subprocess.run(at_cmd, shell=True, capture_output=True, timeout=30)
                    utils.print_info(f"Block will be removed in {duration} seconds")
                
                return True
            else:
                utils.print_error(f"Failed to block IP {ip_address}: {result.stderr}")
                return False
                
    except Exception as e:
        utils.print_error(f"Failed to block IP {ip_address}: {e}")
        return False


def kill_suspicious_process(pid: int, force: bool = False) -> bool:
    """
    Kill or suspend a suspicious process.
    
    Args:
        pid: Process ID to kill
        force: Force kill if True, graceful termination if False
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not utils.check_admin_privileges():
            utils.print_error("Administrative privileges required to kill processes")
            return False
        
        # Get process info
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            process_cmdline = ' '.join(process.cmdline()) if process.cmdline() else 'Unknown'
        except psutil.NoSuchProcess:
            utils.print_error(f"Process {pid} not found")
            return False
        
        utils.print_warning(f"Attempting to kill process: {process_name} (PID: {pid})")
        utils.print_info(f"Command line: {process_cmdline}")
        
        if force:
            # Force kill
            process.kill()
            utils.print_success(f"Force killed process {pid} ({process_name})")
        else:
            # Graceful termination
            process.terminate()
            
            # Wait for termination
            try:
                process.wait(timeout=10)
                utils.print_success(f"Terminated process {pid} ({process_name})")
            except psutil.TimeoutExpired:
                # Force kill if graceful termination fails
                process.kill()
                utils.print_warning(f"Force killed process {pid} ({process_name}) after timeout")
        
        return True
        
    except Exception as e:
        utils.print_error(f"Failed to kill process {pid}: {e}")
        return False


def suspend_suspicious_process(pid: int) -> bool:
    """
    Suspend a suspicious process.
    
    Args:
        pid: Process ID to suspend
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not utils.check_admin_privileges():
            utils.print_error("Administrative privileges required to suspend processes")
            return False
        
        # Get process info
        try:
            process = psutil.Process(pid)
            process_name = process.name()
        except psutil.NoSuchProcess:
            utils.print_error(f"Process {pid} not found")
            return False
        
        utils.print_warning(f"Suspending process: {process_name} (PID: {pid})")
        
        # Suspend process
        process.suspend()
        utils.print_success(f"Suspended process {pid} ({process_name})")
        
        return True
        
    except Exception as e:
        utils.print_error(f"Failed to suspend process {pid}: {e}")
        return False


def list_quarantined_files() -> List[Dict]:
    """List all quarantined files."""
    quarantine_dir = os.path.join(os.getcwd(), "quarantine")
    log_file = os.path.join(quarantine_dir, "quarantine_log.json")
    
    try:
        with open(log_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def restore_quarantined_file(quarantine_path: str, restore_path: str = None) -> bool:
    """
    Restore a quarantined file.
    
    Args:
        quarantine_path: Path to quarantined file
        restore_path: Path to restore to (optional, uses original path if not specified)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not os.path.exists(quarantine_path):
            utils.print_error(f"Quarantined file not found: {quarantine_path}")
            return False
        
        # Get original path from quarantine log
        quarantine_dir = os.path.join(os.getcwd(), "quarantine")
        log_file = os.path.join(quarantine_dir, "quarantine_log.json")
        
        try:
            with open(log_file, 'r') as f:
                log_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            utils.print_error("Quarantine log not found")
            return False
        
        # Find the file in quarantine log
        original_path = None
        for entry in log_data:
            if entry.get('quarantine_path') == quarantine_path:
                original_path = entry.get('original_path')
                break
        
        if not original_path:
            utils.print_error("File not found in quarantine log")
            return False
        
        # Determine restore path
        if not restore_path:
            restore_path = original_path
        
        # Create directory if it doesn't exist
        restore_dir = os.path.dirname(restore_path)
        if restore_dir and not os.path.exists(restore_dir):
            os.makedirs(restore_dir, exist_ok=True)
        
        # Restore file
        import shutil
        shutil.move(quarantine_path, restore_path)
        
        # Remove from quarantine log
        log_data = [entry for entry in log_data if entry.get('quarantine_path') != quarantine_path]
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        utils.print_success(f"File restored: {quarantine_path} -> {restore_path}")
        return True
        
    except Exception as e:
        utils.print_error(f"Failed to restore file {quarantine_path}: {e}")
        return False


def main(args):
    """Main function for IR module."""
    utils.print_banner()
    utils.print_section("Incident Response Snapshot")
    
    utils.print_info("Collecting system information...")
    system_info = collect_system_information()
    
    utils.print_info("Collecting process information...")
    processes = collect_process_information()
    
    utils.print_info("Collecting network information...")
    connections = collect_network_information()
    
    utils.print_info("Collecting file information...")
    files = collect_file_information()
    
    utils.print_info("Collecting user information...")
    users = collect_user_information()
    
    # Generate report
    report = generate_ir_report(processes, connections, files, users, system_info)
    
    # Display report
    display_ir_report(report)
    
    # Handle containment operations
    if args.quarantine or args.block_ip or args.kill_process or args.suspend_process or args.list_quarantined or args.restore_file:
        utils.print_section("Live Response Containment")
        
        # File quarantine
        if args.quarantine:
            utils.print_info("Scanning for suspicious files...")
            suspicious_files = []
            
            # Find suspicious files (recent executables in temp directories)
            for file_info in files:
                if (file_info['path'].lower().endswith(('.exe', '.dll', '.bat', '.cmd', '.ps1')) and
                    any(temp_dir in file_info['path'].lower() for temp_dir in ['temp', 'tmp', 'downloads'])):
                    suspicious_files.append(file_info)
            
            if suspicious_files:
                utils.print_warning(f"Found {len(suspicious_files)} potentially suspicious files")
                for file_info in suspicious_files[:5]:  # Limit to first 5
                    print(f"\nSuspicious file: {file_info['path']}")
                    print(f"  Size: {file_info['size_formatted']}")
                    print(f"  Modified: {file_info['modified_time']}")
                    if file_info.get('hash'):
                        print(f"  Hash: {file_info['hash']}")
                    
                    # Auto-quarantine (in real implementation, this would be interactive)
                    if quarantine_file(file_info['path']):
                        utils.print_success(f"Quarantined: {file_info['path']}")
            else:
                utils.print_info("No suspicious files found for quarantine")
        
        # IP blocking
        if args.block_ip:
            utils.print_info(f"Blocking IP address: {args.block_ip}")
            if block_ip_address(args.block_ip, args.block_duration):
                utils.print_success(f"Successfully blocked IP {args.block_ip}")
            else:
                utils.print_error(f"Failed to block IP {args.block_ip}")
        
        # Process killing
        if args.kill_process:
            utils.print_info(f"Killing process: {args.kill_process}")
            if kill_suspicious_process(args.kill_process, args.force_kill):
                utils.print_success(f"Successfully killed process {args.kill_process}")
            else:
                utils.print_error(f"Failed to kill process {args.kill_process}")
        
        # Process suspension
        if args.suspend_process:
            utils.print_info(f"Suspending process: {args.suspend_process}")
            if suspend_suspicious_process(args.suspend_process):
                utils.print_success(f"Successfully suspended process {args.suspend_process}")
            else:
                utils.print_error(f"Failed to suspend process {args.suspend_process}")
        
        # List quarantined files
        if args.list_quarantined:
            utils.print_info("Listing quarantined files...")
            quarantined_files = list_quarantined_files()
            if quarantined_files:
                utils.print_section(f"Quarantined Files: {len(quarantined_files)}")
                for i, file_info in enumerate(quarantined_files, 1):
                    print(f"\n{i}. Original: {file_info.get('original_path', 'Unknown')}")
                    print(f"   Quarantined: {file_info.get('quarantine_path', 'Unknown')}")
                    print(f"   Time: {file_info.get('quarantine_time', 'Unknown')}")
                    print(f"   Size: {file_info.get('file_size', 'Unknown')} bytes")
                    if file_info.get('file_hash'):
                        print(f"   Hash: {file_info['file_hash']}")
            else:
                utils.print_info("No quarantined files found")
        
        # Restore quarantined file
        if args.restore_file:
            utils.print_info(f"Restoring file: {args.restore_file}")
            if restore_quarantined_file(args.restore_file, args.restore_path):
                utils.print_success(f"Successfully restored file {args.restore_file}")
            else:
                utils.print_error(f"Failed to restore file {args.restore_file}")
    
    # Save report with enhanced export options
    export_format = getattr(args, 'export_format', 'json')
    compress = getattr(args, 'compress', False)
    
    utils.print_info(f"Saving report to {args.output}")
    utils.export_report_with_metadata(
        report, 
        'ir', 
        export_format, 
        args.output, 
        compress
    )
    
    utils.print_success("Incident response snapshot completed")


if __name__ == "__main__":
    # For testing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--quarantine', action='store_true')
    parser.add_argument('--output', default='ir_report.json')
    parser.add_argument('--include-memory', action='store_true')
    args = parser.parse_args()
    main(args)
