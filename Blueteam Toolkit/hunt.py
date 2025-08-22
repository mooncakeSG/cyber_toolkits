"""
Threat Hunting Module for the Blue Team CLI Toolkit.
Implements hunting queries mapped to MITRE ATT&CK techniques.
"""

import os
import sys
import platform
import subprocess
import json
import yaml
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import utils
import psutil


# MITRE ATT&CK hunting queries
HUNTING_QUERIES = {
    'T1053': {  # Scheduled Task/Job
        'name': 'Scheduled Task/Job',
        'description': 'Hunt for suspicious scheduled tasks and cron jobs',
        'windows': [
            'Get-ScheduledTask | Where-Object {$_.State -eq "Ready" -or $_.State -eq "Running"} | Select-Object TaskName, TaskPath, State, LastRunTime',
            'Get-WmiObject -Class Win32_ScheduledJob | Select-Object Name, Command, StartTime, Status',
            'schtasks /query /fo csv /v'
        ],
        'linux': [
            'crontab -l',
            'ls -la /etc/cron.d/',
            'ls -la /var/spool/cron/crontabs/',
            'systemctl list-timers --all'
        ]
    },
    
    'T1003': {  # OS Credential Dumping
        'name': 'OS Credential Dumping',
        'description': 'Hunt for credential dumping activities',
        'windows': [
            'Get-Process | Where-Object {$_.ProcessName -like "*mimikatz*" -or $_.ProcessName -like "*wce*" -or $_.ProcessName -like "*procdump*"}',
            'Get-Process | Where-Object {$_.ProcessName -like "*lsass*"} | Select-Object ProcessName, Id, StartTime',
            'Get-WmiObject -Class Win32_Process | Where-Object {$_.Name -like "*mimikatz*" -or $_.Name -like "*wce*"}'
        ],
        'linux': [
            'ps aux | grep -i "mimikatz\|wce\|procdump"',
            'ps aux | grep -i "gdb\|strace" | grep -v grep',
            'find /tmp -name "*mimikatz*" -o -name "*wce*" 2>/dev/null'
        ]
    },
    
    'T1055': {  # Process Injection
        'name': 'Process Injection',
        'description': 'Hunt for process injection techniques',
        'windows': [
            'Get-Process | Where-Object {$_.Modules.Count -gt 50} | Select-Object ProcessName, Id, Modules',
            'Get-WmiObject -Class Win32_Process | Where-Object {$_.CommandLine -like "*VirtualAlloc*" -or $_.CommandLine -like "*WriteProcessMemory*"}',
            'tasklist /fi "memusage gt 100000" /fo csv'
        ],
        'linux': [
            'ps aux --sort=-%mem | head -20',
            'lsof -p $(ps aux | grep -v grep | grep -E "(gdb|strace|ptrace)" | awk "{print $2}") 2>/dev/null',
            'find /proc -name "maps" -exec grep -l "rwx" {} \\; 2>/dev/null'
        ]
    },
    
    'T1071': {  # Application Layer Protocol
        'name': 'Application Layer Protocol',
        'description': 'Hunt for suspicious network communication',
        'windows': [
            'netstat -ano | findstr "ESTABLISHED"',
            'Get-NetTCPConnection | Where-Object {$_.State -eq "Established"} | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State, OwningProcess',
            'Get-Process | Where-Object {$_.ProcessName -like "*powershell*" -or $_.ProcessName -like "*cmd*"} | Select-Object ProcessName, Id, StartTime'
        ],
        'linux': [
            'netstat -tuln | grep ESTABLISHED',
            'ss -tuln | grep ESTAB',
            'lsof -i -P | grep ESTABLISHED',
            'ps aux | grep -E "(curl|wget|nc|netcat)" | grep -v grep'
        ]
    },
    
    'T1059': {  # Command and Scripting Interpreter
        'name': 'Command and Scripting Interpreter',
        'description': 'Hunt for suspicious command execution',
        'windows': [
            'Get-Process | Where-Object {$_.ProcessName -like "*powershell*" -or $_.ProcessName -like "*cmd*" -or $_.ProcessName -like "*wscript*"} | Select-Object ProcessName, Id, StartTime, CommandLine',
            'Get-WmiObject -Class Win32_Process | Where-Object {$_.Name -like "*powershell*" -or $_.Name -like "*cmd*"} | Select-Object Name, ProcessId, CommandLine',
            'Get-EventLog -LogName Security -InstanceId 4688 | Select-Object TimeGenerated, Message'
        ],
        'linux': [
            'ps aux | grep -E "(bash|sh|python|perl|ruby)" | grep -v grep',
            'history | tail -50',
            'find /tmp -name "*.sh" -o -name "*.py" -o -name "*.pl" 2>/dev/null',
            'cat ~/.bash_history | tail -50'
        ]
    },
    
    'T1064': {  # Scripted Execution
        'name': 'Scripted Execution',
        'description': 'Hunt for script execution and persistence',
        'windows': [
            'Get-ChildItem -Path "C:\\Users\\*\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup" -Recurse',
            'Get-ChildItem -Path "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup" -Recurse',
            'Get-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"',
            'Get-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"'
        ],
        'linux': [
            'ls -la ~/.config/autostart/',
            'systemctl list-unit-files --type=service --state=enabled',
            'find /etc/init.d/ -type f -executable',
            'crontab -l 2>/dev/null'
        ]
    },
    
    'T1083': {  # File and Directory Discovery
        'name': 'File and Directory Discovery',
        'description': 'Hunt for file system reconnaissance',
        'windows': [
            'Get-ChildItem -Path "C:\\Users\\*\\Desktop" -Recurse | Where-Object {$_.LastWriteTime -gt (Get-Date).AddDays(-1)}',
            'Get-ChildItem -Path "C:\\Users\\*\\Documents" -Recurse | Where-Object {$_.LastWriteTime -gt (Get-Date).AddDays(-1)}',
            'Get-ChildItem -Path "C:\\Temp" -Recurse 2>$null | Where-Object {$_.LastWriteTime -gt (Get-Date).AddDays(-1)}'
        ],
        'linux': [
            'find /home -type f -mtime -1 2>/dev/null | head -50',
            'find /tmp -type f -mtime -1 2>/dev/null | head -50',
            'ls -la /home/*/Desktop/ 2>/dev/null',
            'ls -la /home/*/Documents/ 2>/dev/null'
        ]
    },
    
    'T1016': {  # System Network Configuration Discovery
        'name': 'System Network Configuration Discovery',
        'description': 'Hunt for network reconnaissance activities',
        'windows': [
            'ipconfig /all',
            'route print',
            'netstat -r',
            'Get-NetAdapter | Select-Object Name, Status, InterfaceDescription'
        ],
        'linux': [
            'ifconfig -a',
            'ip route show',
            'netstat -r',
            'cat /etc/resolv.conf'
        ]
    }
}


def list_available_techniques():
    """List all available MITRE ATT&CK Hunting Techniques."""
    utils.print_section("Available MITRE ATT&CK Hunting Techniques")
    
    for technique_id, technique_info in HUNTING_QUERIES.items():
        print(f"\n{technique_id}: {technique_info['name']}")
        print(f"   Description: {technique_info['description']}")
        print(f"   Supported OS: {', '.join(technique_info.keys()) if 'windows' in technique_info and 'linux' in technique_info else list(technique_info.keys())[0]}")


def run_hunting_query(technique_id: str, os_type: str = None, verbose: bool = False) -> Dict[str, Any]:
    """Run a specific hunting query for a MITRE ATT&CK technique."""
    if technique_id not in HUNTING_QUERIES:
        utils.print_error(f"Unknown technique ID: {technique_id}")
        return {}
    
    technique_info = HUNTING_QUERIES[technique_id]
    
    # Determine OS type if not specified
    if not os_type:
        os_type = 'windows' if platform.system() == 'Windows' else 'linux'
    
    if os_type not in technique_info:
        utils.print_error(f"Technique {technique_id} not supported on {os_type}")
        return {}
    
    queries = technique_info[os_type]
    results = {
        'technique_id': technique_id,
        'technique_name': technique_info['name'],
        'description': technique_info['description'],
        'os_type': os_type,
        'queries': [],
        'suspicious_findings': []
    }
    
    utils.print_info(f"Running hunting queries for {technique_id}: {technique_info['name']}")
    
    for i, query in enumerate(queries, 1):
        utils.print_info(f"Executing query {i}/{len(queries)}")
        
        if verbose:
            print(f"   Query: {query}")
        
        try:
            if os_type == 'windows':
                # Execute PowerShell command
                result = subprocess.run(
                    ["powershell", "-Command", query],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                # Execute shell command
                result = subprocess.run(
                    query,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            query_result = {
                'query': query,
                'returncode': result.returncode,
                'stdout': result.stdout.strip(),
                'stderr': result.stderr.strip(),
                'success': result.returncode == 0
            }
            
            results['queries'].append(query_result)
            
            # Analyze results for suspicious patterns
            if result.returncode == 0 and result.stdout.strip():
                suspicious_patterns = analyze_hunting_results(result.stdout, technique_id, os_type)
                if suspicious_patterns:
                    results['suspicious_findings'].extend(suspicious_patterns)
            
        except subprocess.TimeoutExpired:
            utils.print_warning(f"Query {i} timed out")
            results['queries'].append({
                'query': query,
                'returncode': -1,
                'stdout': '',
                'stderr': 'Command timed out',
                'success': False
            })
        except Exception as e:
            utils.print_error(f"Error executing query {i}: {e}")
            results['queries'].append({
                'query': query,
                'returncode': -1,
                'stdout': '',
                'stderr': str(e),
                'success': False
            })
    
    return results


def analyze_hunting_results(output: str, technique_id: str, os_type: str) -> List[Dict]:
    """Analyze hunting query results for suspicious patterns."""
    suspicious_findings = []
    
    # Define suspicious patterns for each technique
    suspicious_patterns = {
        'T1053': {  # Scheduled Task/Job
            'windows': ['mimikatz', 'wce', 'procdump', 'powershell', 'cmd', 'rundll32'],
            'linux': ['mimikatz', 'wce', 'procdump', 'bash', 'python', 'perl']
        },
        'T1003': {  # OS Credential Dumping
            'windows': ['mimikatz', 'wce', 'procdump', 'lsass', 'sam', 'system'],
            'linux': ['mimikatz', 'wce', 'procdump', 'gdb', 'strace', 'ptrace']
        },
        'T1055': {  # Process Injection
            'windows': ['VirtualAlloc', 'WriteProcessMemory', 'CreateRemoteThread', 'SetWindowsHookEx'],
            'linux': ['ptrace', 'gdb', 'strace', 'inject', 'hook']
        },
        'T1071': {  # Application Layer Protocol
            'windows': ['powershell', 'cmd', 'wscript', 'cscript', 'rundll32'],
            'linux': ['curl', 'wget', 'nc', 'netcat', 'socat']
        },
        'T1059': {  # Command and Scripting Interpreter
            'windows': ['powershell', 'cmd', 'wscript', 'cscript', 'rundll32'],
            'linux': ['bash', 'sh', 'python', 'perl', 'ruby']
        },
        'T1064': {  # Scripted Execution
            'windows': ['startup', 'autostart', 'registry', 'scheduled'],
            'linux': ['autostart', 'systemd', 'init.d', 'cron']
        },
        'T1083': {  # File and Directory Discovery
            'windows': ['desktop', 'documents', 'downloads', 'temp'],
            'linux': ['desktop', 'documents', 'downloads', 'tmp']
        },
        'T1016': {  # System Network Configuration Discovery
            'windows': ['ipconfig', 'route', 'netstat', 'arp'],
            'linux': ['ifconfig', 'ip', 'route', 'netstat']
        }
    }
    
    patterns = suspicious_patterns.get(technique_id, {}).get(os_type, [])
    
    for pattern in patterns:
        if pattern.lower() in output.lower():
            suspicious_findings.append({
                'pattern': pattern,
                'context': extract_context(output, pattern),
                'severity': 'medium'
            })
    
    return suspicious_findings


def extract_context(output: str, pattern: str, context_lines: int = 2) -> str:
    """Extract context around a suspicious pattern."""
    lines = output.split('\n')
    context = []
    
    for i, line in enumerate(lines):
        if pattern.lower() in line.lower():
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            context.extend(lines[start:end])
    
    return '\n'.join(context) if context else output[:200] + '...'


def get_process_list() -> List[Dict[str, Any]]:
    """Get list of running processes with detailed information."""
    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time', 'memory_info', 'cpu_percent']):
            try:
                proc_info = proc.info
                # Convert command line list to string
                if proc_info['cmdline']:
                    proc_info['CommandLine'] = ' '.join(proc_info['cmdline'])
                else:
                    proc_info['CommandLine'] = proc_info['name']
                
                # Add process name for compatibility
                proc_info['ProcessName'] = proc_info['name']
                
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        utils.print_error(f"Failed to get process list: {e}")
    
    return processes


def get_network_connections() -> List[Dict[str, Any]]:
    """Get network connections for Sigma rule matching."""
    connections = []
    try:
        for conn in psutil.net_connections():
            try:
                conn_info = {
                    'LocalAddress': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                    'RemoteAddress': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                    'LocalPort': conn.laddr.port if conn.laddr else None,
                    'RemotePort': conn.raddr.port if conn.raddr else None,
                    'Status': conn.status,
                    'PID': conn.pid,
                    'Family': conn.family,
                    'Type': conn.type
                }
                connections.append(conn_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        utils.print_error(f"Failed to get network connections: {e}")
    
    return connections


def display_hunting_results(results: Dict[str, Any]):
    """Display hunting results in a formatted way."""
    if not results:
        utils.print_warning("No hunting results to display")
        return
    
    utils.print_section(f"Hunting Results: {results['technique_id']}")
    print(f"Technique: {results['technique_name']}")
    print(f"Description: {results['description']}")
    print(f"OS Type: {results['os_type']}")
    
    # Show query results
    print(f"\nExecuted {len(results['queries'])} queries:")
    for i, query_result in enumerate(results['queries'], 1):
        status = "✓" if query_result['success'] else "✗"
        print(f"\n{i}. [{status}] Query {i}")
        
        if query_result['success'] and query_result['stdout']:
            print(f"   Output: {query_result['stdout'][:200]}{'...' if len(query_result['stdout']) > 200 else ''}")
        elif not query_result['success']:
            print(f"   Error: {query_result['stderr']}")
    
    # Show suspicious findings
    if results['suspicious_findings']:
        utils.print_section("Suspicious Findings")
        for i, finding in enumerate(results['suspicious_findings'], 1):
            print(f"\n{i}. Pattern: {finding['pattern']}")
            print(f"   Severity: {finding['severity']}")
            print(f"   Context: {finding['context'][:150]}...")
    else:
        print("\nNo suspicious findings detected.")


def parse_sigma_rule(rule_path: str) -> Dict[str, Any]:
    """
    Parse a Sigma rule file and extract detection logic.
    
    Args:
        rule_path: Path to the Sigma rule file (.yml)
        
    Returns:
        Dictionary containing parsed rule information
    """
    try:
        with open(rule_path, 'r', encoding='utf-8') as f:
            rule_content = yaml.safe_load(f)
        
        # Extract key information from Sigma rule
        rule_info = {
            'title': rule_content.get('title', 'Unknown'),
            'id': rule_content.get('id', 'Unknown'),
            'description': rule_content.get('description', ''),
            'author': rule_content.get('author', 'Unknown'),
            'date': rule_content.get('date', ''),
            'tags': rule_content.get('tags', []),
            'logsource': rule_content.get('logsource', {}),
            'detection': rule_content.get('detection', {}),
            'falsepositives': rule_content.get('falsepositives', []),
            'level': rule_content.get('level', 'medium'),
            'status': rule_content.get('status', 'experimental')
        }
        
        return rule_info
    except Exception as e:
        utils.print_error(f"Failed to parse Sigma rule {rule_path}: {e}")
        return None

def validate_sigma_rule(rule_info: Dict[str, Any]) -> bool:
    """
    Validate a parsed Sigma rule for required fields and structure.
    
    Args:
        rule_info: Parsed rule information
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['title', 'detection']
    
    for field in required_fields:
        if field not in rule_info or not rule_info[field]:
            utils.print_warning(f"Sigma rule missing required field: {field}")
            return False
    
    # Check for detection logic
    detection = rule_info.get('detection', {})
    if not detection.get('selection') and not detection.get('condition'):
        utils.print_warning("Sigma rule missing detection logic")
        return False
    
    return True

def execute_sigma_rule(rule_info: Dict[str, Any], os_type: str = None) -> List[Dict[str, Any]]:
    """
    Execute a Sigma rule against system data.
    
    Args:
        rule_info: Parsed rule information
        os_type: Operating system type (windows/linux)
        
    Returns:
        List of matches found
    """
    if not os_type:
        os_type = platform.system().lower()
    
    detection = rule_info.get('detection', {})
    selection = detection.get('selection', {})
    condition = detection.get('condition', 'selection')
    
    matches = []
    
    try:
        # Execute based on logsource
        logsource = rule_info.get('logsource', {})
        category = logsource.get('category', '')
        product = logsource.get('product', '')
        
        if category == 'process_creation' or product == 'windows':
            matches.extend(execute_windows_rule(rule_info, selection, condition))
        elif category == 'process_creation' or product == 'linux':
            matches.extend(execute_linux_rule(rule_info, selection, condition))
        else:
            # Generic execution
            matches.extend(execute_generic_rule(rule_info, selection, condition))
            
    except Exception as e:
        utils.print_error(f"Failed to execute Sigma rule: {e}")
    
    return matches

def execute_windows_rule(rule_info: Dict[str, Any], selection: Dict, condition: str) -> List[Dict[str, Any]]:
    """Execute Sigma rule against Windows data."""
    matches = []
    
    try:
        # Get process information
        processes = get_process_list()
        
        for process in processes:
            if matches_selection_criteria(process, selection):
                matches.append({
                    'rule_title': rule_info.get('title', 'Unknown'),
                    'rule_id': rule_info.get('id', 'Unknown'),
                    'match_type': 'process',
                    'data': process,
                    'timestamp': datetime.now().isoformat()
                })
        
        # Check Windows Event Logs if available
        if hasattr(utils, 'get_windows_event_logs'):
            try:
                event_logs = utils.get_windows_event_logs(100)  # Get last 100 events
                for event in event_logs:
                    if matches_selection_criteria(event, selection):
                        matches.append({
                            'rule_title': rule_info.get('title', 'Unknown'),
                            'rule_id': rule_info.get('id', 'Unknown'),
                            'match_type': 'event_log',
                            'data': event,
                            'timestamp': datetime.now().isoformat()
                        })
            except:
                pass  # Event logs might not be accessible
                
    except Exception as e:
        utils.print_error(f"Error executing Windows rule: {e}")
    
    return matches

def execute_linux_rule(rule_info: Dict[str, Any], selection: Dict, condition: str) -> List[Dict[str, Any]]:
    """Execute Sigma rule against Linux data."""
    matches = []
    
    try:
        # Get process information
        processes = get_process_list()
        
        for process in processes:
            if matches_selection_criteria(process, selection):
                matches.append({
                    'rule_title': rule_info.get('title', 'Unknown'),
                    'match_type': 'process',
                    'data': process,
                    'timestamp': datetime.now().isoformat()
                })
        
        # Check system logs if available
        if os.path.exists('/var/log/auth.log'):
            try:
                with open('/var/log/auth.log', 'r') as f:
                    auth_logs = f.readlines()[-100:]  # Last 100 lines
                
                for line in auth_logs:
                    if matches_selection_criteria({'log_line': line}, selection):
                        matches.append({
                            'rule_title': rule_info.get('title', 'Unknown'),
                            'rule_id': rule_info.get('id', 'Unknown'),
                            'match_type': 'auth_log',
                            'data': {'log_line': line.strip()},
                            'timestamp': datetime.now().isoformat()
                        })
            except:
                pass
                
    except Exception as e:
        utils.print_error(f"Error executing Linux rule: {e}")
    
    return matches

def execute_generic_rule(rule_info: Dict[str, Any], selection: Dict, condition: str) -> List[Dict[str, Any]]:
    """Execute Sigma rule using generic data sources."""
    matches = []
    
    try:
        # Get basic system information
        processes = get_process_list()
        network_connections = get_network_connections()
        
        # Check processes
        for process in processes:
            if matches_selection_criteria(process, selection):
                matches.append({
                    'rule_title': rule_info.get('title', 'Unknown'),
                    'rule_id': rule_info.get('id', 'Unknown'),
                    'match_type': 'process',
                    'data': process,
                    'timestamp': datetime.now().isoformat()
                })
        
        # Check network connections
        for conn in network_connections:
            if matches_selection_criteria(conn, selection):
                matches.append({
                    'rule_title': rule_info.get('title', 'Unknown'),
                    'rule_id': rule_info.get('id', 'Unknown'),
                    'match_type': 'network',
                    'data': conn,
                    'timestamp': datetime.now().isoformat()
                })
                
    except Exception as e:
        utils.print_error(f"Error executing generic rule: {e}")
    
    return matches

def matches_selection_criteria(data: Dict[str, Any], selection: Dict) -> bool:
    """
    Check if data matches the selection criteria from Sigma rule.
    
    Args:
        data: Data to check
        selection: Selection criteria from Sigma rule
        
    Returns:
        True if matches, False otherwise
    """
    try:
        for field, criteria in selection.items():
            if field not in data:
                return False
            
            data_value = data[field]
            
            # Handle different types of criteria
            if isinstance(criteria, dict):
                # Handle operators like contains, startswith, endswith
                for operator, value in criteria.items():
                    if operator == 'contains':
                        if isinstance(data_value, str) and isinstance(value, str):
                            if value.lower() not in data_value.lower():
                                return False
                        else:
                            return False
                    elif operator == 'startswith':
                        if isinstance(data_value, str) and isinstance(value, str):
                            if not data_value.lower().startswith(value.lower()):
                                return False
                        else:
                            return False
                    elif operator == 'endswith':
                        if isinstance(data_value, str) and isinstance(value, str):
                            if not data_value.lower().endswith(value.lower()):
                                return False
                        else:
                            return False
                    elif operator == 're':
                        if isinstance(data_value, str):
                            if not re.search(value, data_value, re.IGNORECASE):
                                return False
                        else:
                            return False
                    else:
                        # Unknown operator, try direct comparison
                        if data_value != value:
                            return False
            else:
                # Direct value comparison
                if data_value != criteria:
                    return False
        
        return True
        
    except Exception as e:
        utils.print_error(f"Error checking selection criteria: {e}")
        return False

def load_sigma_rules_from_directory(directory: str) -> List[Dict[str, Any]]:
    """
    Load all Sigma rules from a directory.
    
    Args:
        directory: Directory containing Sigma rule files
        
    Returns:
        List of parsed and validated rules
    """
    rules = []
    
    try:
        if not os.path.exists(directory):
            utils.print_error(f"Sigma rules directory not found: {directory}")
            return rules
        
        for filename in os.listdir(directory):
            if filename.endswith(('.yml', '.yaml')):
                rule_path = os.path.join(directory, filename)
                rule_info = parse_sigma_rule(rule_path)
                
                if rule_info and validate_sigma_rule(rule_info):
                    rules.append(rule_info)
                    utils.print_info(f"Loaded Sigma rule: {rule_info.get('title', filename)}")
                else:
                    utils.print_warning(f"Invalid Sigma rule: {filename}")
                    
    except Exception as e:
        utils.print_error(f"Error loading Sigma rules: {e}")
    
    return rules

def display_sigma_results(results: List[Dict[str, Any]], rule_info: Dict[str, Any] = None):
    """Display Sigma rule execution results."""
    if not results:
        utils.print_info("No matches found for Sigma rule")
        return
    
    utils.print_section(f"Sigma Rule Results: {len(results)} matches")
    
    if rule_info:
        utils.print_info(f"Rule: {rule_info.get('title', 'Unknown')}")
        utils.print_info(f"ID: {rule_info.get('id', 'Unknown')}")
        utils.print_info(f"Level: {rule_info.get('level', 'medium')}")
        utils.print_info(f"Description: {rule_info.get('description', 'No description')}")
        print()
    
    for i, match in enumerate(results, 1):
        utils.print_warning(f"Match {i}:")
        utils.print_info(f"  Type: {match.get('match_type', 'unknown')}")
        utils.print_info(f"  Timestamp: {match.get('timestamp', 'unknown')}")
        
        data = match.get('data', {})
        if isinstance(data, dict):
            for key, value in data.items():
                if key not in ['timestamp', 'rule_title', 'rule_id']:
                    utils.print_info(f"  {key}: {value}")
        else:
            utils.print_info(f"  Data: {data}")
        print()


def main(args):
    """Main function for threat hunting module."""
    utils.print_banner()
    utils.print_section("Threat Hunting")
    
    results = []
    
    # Handle Sigma rule execution
    if hasattr(args, 'sigma') and args.sigma:
        if os.path.isfile(args.sigma):
            # Single Sigma rule file
            utils.print_info(f"Executing Sigma rule: {args.sigma}")
            rule_info = parse_sigma_rule(args.sigma)
            
            if rule_info and validate_sigma_rule(rule_info):
                results = execute_sigma_rule(rule_info, getattr(args, 'os', None))
                display_sigma_results(results, rule_info)
            else:
                utils.print_error("Invalid Sigma rule file")
                return
        elif os.path.isdir(args.sigma):
            # Directory of Sigma rules
            utils.print_info(f"Loading Sigma rules from directory: {args.sigma}")
            rules = load_sigma_rules_from_directory(args.sigma)
            
            if not rules:
                utils.print_error("No valid Sigma rules found in directory")
                return
            
            all_results = []
            for rule in rules:
                utils.print_info(f"Executing rule: {rule.get('title', 'Unknown')}")
                rule_results = execute_sigma_rule(rule, getattr(args, 'os', None))
                all_results.extend(rule_results)
                
                if rule_results:
                    display_sigma_results(rule_results, rule)
            
            results = all_results
        else:
            utils.print_error(f"Sigma rule path not found: {args.sigma}")
            return
    
    # Handle traditional MITRE ATT&CK hunting
    elif hasattr(args, 'technique') and args.technique:
        utils.print_info(f"Running hunting query for technique: {args.technique}")
        results = run_hunting_query(args.technique)
        
        if results:
            display_hunting_results(results)
        else:
            utils.print_error("Failed to run hunting queries")
    
    # Export results if requested
    if hasattr(args, 'export') and args.export:
        export_format = getattr(args, 'export_format', 'json')
        compress = getattr(args, 'compress', False)
        
        # For Sigma rules, always export results (even if empty)
        if hasattr(args, 'sigma') and args.sigma:
            export_data = {
                'sigma_rules_executed': True,
                'rules_processed': len(rules) if 'rules' in locals() else 1,
                'matches_found': len(results),
                'results': results,
                'execution_timestamp': datetime.now().isoformat()
            }
        else:
            export_data = results
        
        utils.export_report_with_metadata(
            export_data, 
            'hunt', 
            export_format, 
            args.export, 
            compress
        )
    
    utils.print_success("Threat hunting completed")


if __name__ == "__main__":
    # For testing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--technique', type=str)
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    main(args)
