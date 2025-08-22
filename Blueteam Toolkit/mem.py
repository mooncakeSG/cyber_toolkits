"""
Memory Forensics Module for the Blue Team CLI Toolkit.
Provides memory analysis capabilities using system tools and APIs.
"""

import os
import sys
import platform
import subprocess
import psutil
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import utils


def get_memory_info() -> Dict[str, Any]:
    """Get basic memory information."""
    try:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total_memory_gb': round(memory.total / (1024**3), 2),
            'available_memory_gb': round(memory.available / (1024**3), 2),
            'used_memory_gb': round(memory.used / (1024**3), 2),
            'memory_percent': memory.percent,
            'swap_total_gb': round(swap.total / (1024**3), 2),
            'swap_used_gb': round(swap.used / (1024**3), 2),
            'swap_percent': swap.percent
        }
    except Exception as e:
        utils.print_error(f"Error getting memory info: {e}")
        return {}


def list_processes_with_memory() -> List[Dict]:
    """List all processes with memory information."""
    processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent', 'create_time']):
            try:
                proc_info = proc.info
                memory_mb = round(proc_info['memory_info'].rss / (1024**2), 2) if proc_info['memory_info'] else 0
                
                processes.append({
                    'pid': proc_info['pid'],
                    'name': proc_info['name'],
                    'memory_mb': memory_mb,
                    'cpu_percent': proc_info['cpu_percent'],
                    'create_time': datetime.fromtimestamp(proc_info['create_time']).strftime('%Y-%m-%d %H:%M:%S'),
                    'suspicious': utils.is_suspicious_process(proc_info['name'])
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
        # Sort by memory usage (descending)
        processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        
    except Exception as e:
        utils.print_error(f"Error listing processes: {e}")
    
    return processes


def get_process_memory_map(pid: int) -> List[Dict]:
    """Get memory map for a specific process."""
    memory_regions = []
    
    try:
        if platform.system() == "Windows":
            # Windows - use wmic to get process memory info
            cmd = f'wmic process where ProcessId={pid} get WorkingSetSize,PageFileUsage /format:csv'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split(',')
                    if len(parts) >= 3:
                        memory_regions.append({
                            'region': 'Working Set',
                            'size_bytes': int(parts[1]) if parts[1].isdigit() else 0,
                            'size_mb': round(int(parts[1]) / (1024**2), 2) if parts[1].isdigit() else 0,
                            'type': 'Private'
                        })
                        memory_regions.append({
                            'region': 'Page File',
                            'size_bytes': int(parts[2]) if parts[2].isdigit() else 0,
                            'size_mb': round(int(parts[2]) / (1024**2), 2) if parts[2].isdigit() else 0,
                            'type': 'Committed'
                        })
        else:
            # Linux - read /proc/{pid}/maps
            maps_file = f"/proc/{pid}/maps"
            if os.path.exists(maps_file):
                try:
                    with open(maps_file, 'r') as f:
                        for line in f:
                            parts = line.strip().split()
                            if len(parts) >= 5:
                                addr_range = parts[0]
                                perms = parts[1]
                                offset = parts[2]
                                dev = parts[3]
                                inode = parts[4]
                                pathname = ' '.join(parts[5:]) if len(parts) > 5 else ''
                                
                                # Calculate size from address range
                                start, end = addr_range.split('-')
                                size = int(end, 16) - int(start, 16)
                                
                                memory_regions.append({
                                    'address_range': addr_range,
                                    'permissions': perms,
                                    'size_bytes': size,
                                    'size_mb': round(size / (1024**2), 2),
                                    'offset': offset,
                                    'pathname': pathname,
                                    'type': 'Private' if 'p' in perms else 'Shared'
                                })
                except (IOError, PermissionError):
                    pass
                    
    except Exception as e:
        utils.print_error(f"Error getting memory map for PID {pid}: {e}")
    
    return memory_regions


def dump_process_memory(pid: int, output_file: str = None) -> bool:
    """Dump process memory to file."""
    try:
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"memory_dump_pid_{pid}_{timestamp}.bin"
        
        utils.print_warning(f"Memory dumping requires elevated privileges and may be resource-intensive")
        
        if platform.system() == "Windows":
            # Windows - use procdump or similar tool
            # Note: This is a placeholder - actual implementation would require procdump
            utils.print_info("Windows memory dumping requires procdump or similar tool")
            utils.print_info(f"Would dump PID {pid} to {output_file}")
            return False
        else:
            # Linux - use gcore or similar
            cmd = f"gcore -o {output_file} {pid}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                utils.print_success(f"Memory dump saved to {output_file}")
                return True
            else:
                utils.print_error(f"Failed to dump memory: {result.stderr}")
                return False
                
    except Exception as e:
        utils.print_error(f"Error dumping process memory: {e}")
        return False


def scan_memory_for_strings(pid: int, search_strings: List[str]) -> List[Dict]:
    """Scan process memory for specific strings."""
    matches = []
    
    try:
        if platform.system() == "Windows":
            # Windows - use PowerShell to search process memory
            # This is a simplified approach - real implementation would be more complex
            utils.print_info("Windows memory string scanning requires specialized tools")
            return []
        else:
            # Linux - use strings command on /proc/{pid}/mem
            mem_file = f"/proc/{pid}/mem"
            if os.path.exists(mem_file):
                for search_string in search_strings:
                    try:
                        cmd = f"strings {mem_file} | grep -i '{search_string}'"
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        
                        if result.returncode == 0 and result.stdout.strip():
                            matches.append({
                                'pid': pid,
                                'search_string': search_string,
                                'matches': result.stdout.strip().split('\n'),
                                'match_count': len(result.stdout.strip().split('\n'))
                            })
                    except Exception:
                        continue
                        
    except Exception as e:
        utils.print_error(f"Error scanning memory for strings: {e}")
    
    return matches


def detect_memory_anomalies() -> List[Dict]:
    """Detect memory-related anomalies."""
    anomalies = []
    
    try:
        # Check for high memory usage
        memory_info = get_memory_info()
        if memory_info.get('memory_percent', 0) > 90:
            anomalies.append({
                'type': 'High Memory Usage',
                'severity': 'high',
                'description': f"Memory usage is {memory_info['memory_percent']}%",
                'recommendation': 'Investigate memory-intensive processes'
            })
        
        # Check for processes with unusual memory patterns
        processes = list_processes_with_memory()
        for proc in processes[:20]:  # Check top 20 processes
            if proc['memory_mb'] > 1000:  # Processes using >1GB
                anomalies.append({
                    'type': 'High Memory Process',
                    'severity': 'medium',
                    'description': f"Process {proc['name']} (PID: {proc['pid']}) using {proc['memory_mb']}MB",
                    'process_info': proc
                })
        
        # Check for suspicious processes in memory
        suspicious_procs = [p for p in processes if p['suspicious']]
        for proc in suspicious_procs:
            anomalies.append({
                'type': 'Suspicious Process in Memory',
                'severity': 'high',
                'description': f"Suspicious process {proc['name']} (PID: {proc['pid']}) detected",
                'process_info': proc
            })
            
    except Exception as e:
        utils.print_error(f"Error detecting memory anomalies: {e}")
    
    return anomalies


def get_memory_statistics() -> Dict[str, Any]:
    """Get comprehensive memory statistics."""
    try:
        memory_info = get_memory_info()
        processes = list_processes_with_memory()
        
        # Calculate statistics
        total_processes = len(processes)
        high_memory_processes = len([p for p in processes if p['memory_mb'] > 500])
        suspicious_processes = len([p for p in processes if p['suspicious']])
        
        # Top memory consumers
        top_consumers = processes[:10]
        
        # Memory distribution
        memory_distribution = {
            '0-100MB': len([p for p in processes if p['memory_mb'] <= 100]),
            '100-500MB': len([p for p in processes if 100 < p['memory_mb'] <= 500]),
            '500MB-1GB': len([p for p in processes if 500 < p['memory_mb'] <= 1024]),
            '1GB+': len([p for p in processes if p['memory_mb'] > 1024])
        }
        
        return {
            'memory_info': memory_info,
            'process_statistics': {
                'total_processes': total_processes,
                'high_memory_processes': high_memory_processes,
                'suspicious_processes': suspicious_processes
            },
            'top_memory_consumers': top_consumers,
            'memory_distribution': memory_distribution
        }
        
    except Exception as e:
        utils.print_error(f"Error getting memory statistics: {e}")
        return {}


def display_memory_info(memory_info: Dict[str, Any]):
    """Display memory information."""
    utils.print_section("Memory Information")
    
    print(f"Total Memory: {memory_info.get('total_memory_gb', 0)} GB")
    print(f"Available Memory: {memory_info.get('available_memory_gb', 0)} GB")
    print(f"Used Memory: {memory_info.get('used_memory_gb', 0)} GB")
    print(f"Memory Usage: {memory_info.get('memory_percent', 0)}%")
    print(f"Swap Total: {memory_info.get('swap_total_gb', 0)} GB")
    print(f"Swap Used: {memory_info.get('swap_used_gb', 0)} GB")
    print(f"Swap Usage: {memory_info.get('swap_percent', 0)}%")


def display_processes_with_memory(processes: List[Dict], limit: int = 20):
    """Display processes with memory information."""
    utils.print_section("Processes with Memory Information")
    
    print(f"Showing top {min(limit, len(processes))} processes by memory usage:")
    print(f"{'PID':<8} {'Name':<25} {'Memory (MB)':<12} {'CPU %':<8} {'Suspicious':<10}")
    print("-" * 70)
    
    for proc in processes[:limit]:
        suspicious_flag = "⚠️" if proc['suspicious'] else " "
        print(f"{proc['pid']:<8} {proc['name'][:24]:<25} {proc['memory_mb']:<12.1f} {proc['cpu_percent']:<8.1f} {suspicious_flag:<10}")


def display_memory_anomalies(anomalies: List[Dict]):
    """Display memory anomalies."""
    if not anomalies:
        utils.print_info("No memory anomalies detected")
        return
    
    utils.print_section("Memory Anomalies")
    
    for i, anomaly in enumerate(anomalies, 1):
        severity_icon = "🔴" if anomaly['severity'] == 'high' else "🟡"
        print(f"\n{i}. {severity_icon} {anomaly['type']}")
        print(f"   Severity: {anomaly['severity']}")
        print(f"   Description: {anomaly['description']}")
        if 'recommendation' in anomaly:
            print(f"   Recommendation: {anomaly['recommendation']}")


def main(args):
    """Main function for memory forensics module."""
    utils.print_banner()
    utils.print_section("Memory Forensics")
    
    # Get basic memory information
    if args.info:
        memory_info = get_memory_info()
        display_memory_info(memory_info)
    
    # List processes with memory
    if args.list_procs:
        processes = list_processes_with_memory()
        display_processes_with_memory(processes, args.limit if hasattr(args, 'limit') else 20)
    
    # Get memory map for specific process
    if args.memory_map:
        if not args.pid:
            utils.print_error("Please specify PID with --pid for memory map")
            return
        
        memory_regions = get_process_memory_map(args.pid)
        if memory_regions:
            utils.print_section(f"Memory Map for PID {args.pid}")
            for region in memory_regions[:10]:  # Show first 10 regions
                print(f"Region: {region.get('region', 'Unknown')}")
                print(f"  Size: {region.get('size_mb', 0)} MB")
                print(f"  Type: {region.get('type', 'Unknown')}")
        else:
            utils.print_warning(f"No memory map available for PID {args.pid}")
    
    # Dump process memory
    if args.dump:
        if not args.pid:
            utils.print_error("Please specify PID with --pid for memory dump")
            return
        
        output_file = args.output if hasattr(args, 'output') else None
        if dump_process_memory(args.pid, output_file):
            utils.print_success(f"Memory dump completed for PID {args.pid}")
        else:
            utils.print_error(f"Failed to dump memory for PID {args.pid}")
    
    # Scan memory for strings
    if args.scan_strings:
        if not args.pid:
            utils.print_error("Please specify PID with --pid for string scanning")
            return
        
        search_strings = args.strings.split(',') if hasattr(args, 'strings') else ['password', 'admin', 'root']
        matches = scan_memory_for_strings(args.pid, search_strings)
        
        if matches:
            utils.print_section(f"Memory String Scan Results for PID {args.pid}")
            for match in matches:
                print(f"\nSearch String: {match['search_string']}")
                print(f"Matches Found: {match['match_count']}")
                for i, result in enumerate(match['matches'][:5], 1):  # Show first 5 matches
                    print(f"  {i}. {result[:100]}...")
        else:
            utils.print_info(f"No string matches found in PID {args.pid}")
    
    # Detect anomalies
    if args.anomalies:
        anomalies = detect_memory_anomalies()
        display_memory_anomalies(anomalies)
    
    # Get comprehensive statistics
    if args.stats:
        stats = get_memory_statistics()
        if stats:
            utils.print_section("Memory Statistics")
            print(f"Total Processes: {stats['process_statistics']['total_processes']}")
            print(f"High Memory Processes: {stats['process_statistics']['high_memory_processes']}")
            print(f"Suspicious Processes: {stats['process_statistics']['suspicious_processes']}")
            
            print(f"\nMemory Distribution:")
            for range_name, count in stats['memory_distribution'].items():
                print(f"  {range_name}: {count} processes")
    
    # If no specific action requested, show overview
    if not any([args.info, args.list_procs, args.memory_map, args.dump, args.scan_strings, args.anomalies, args.stats]):
        utils.print_info("Showing memory overview...")
        
        memory_info = get_memory_info()
        display_memory_info(memory_info)
        
        processes = list_processes_with_memory()
        display_processes_with_memory(processes, 10)
        
        anomalies = detect_memory_anomalies()
        display_memory_anomalies(anomalies)
    
    # Export if requested
    if hasattr(args, 'export') and args.export:
        # Prepare export data
        export_data = {
            'memory_info': get_memory_info(),
            'processes': list_processes_with_memory(),
            'anomalies': detect_memory_anomalies(),
            'statistics': get_memory_statistics()
        }
        
        export_format = getattr(args, 'export_format', 'json')
        compress = getattr(args, 'compress', False)
        
        utils.export_report_with_metadata(
            export_data, 
            'mem', 
            export_format, 
            args.export, 
            compress
        )
    
    utils.print_success("Memory forensics analysis completed")


if __name__ == "__main__":
    # For testing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--info', action='store_true', help='Show memory information')
    parser.add_argument('--list-procs', action='store_true', help='List processes with memory info')
    parser.add_argument('--memory-map', action='store_true', help='Get memory map for process')
    parser.add_argument('--dump', action='store_true', help='Dump process memory')
    parser.add_argument('--scan-strings', action='store_true', help='Scan memory for strings')
    parser.add_argument('--anomalies', action='store_true', help='Detect memory anomalies')
    parser.add_argument('--stats', action='store_true', help='Get memory statistics')
    parser.add_argument('--pid', type=int, help='Process ID for specific operations')
    parser.add_argument('--output', type=str, help='Output file for memory dump')
    parser.add_argument('--strings', type=str, help='Comma-separated strings to search for')
    parser.add_argument('--limit', type=int, default=20, help='Limit number of processes to show')
    args = parser.parse_args()
    main(args)
