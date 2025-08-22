#!/usr/bin/env python3
"""
Blue Team CLI Toolkit
A Python-based command-line toolkit for defensive security operations.
"""

import argparse
import sys
import os
from typing import Dict, Any

# Import our modules
import logs
import hunt
import ir
import ioc
import net
import mem
import siem
import automation
import alerts
import utils


def setup_parser() -> argparse.ArgumentParser:
    """Set up the main argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        description="Blue Team CLI Toolkit - Defensive Security Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py logs --os windows --lines 100
  python main.py hunt --technique T1053
  python main.py hunt --sigma sigma_rules/suspicious_process_creation.yml
  python main.py ir
  python main.py ioc --type ip --value 8.8.8.8 --vt
  python main.py net
  python main.py mem --list-procs
  python main.py siem --type elk --host localhost --alerts
  python main.py automation --add --task-type hunt --schedule-type daily --schedule-value "14:30"
  python main.py alerts --configure --channel slack
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Memory forensics subcommand
    mem_parser = subparsers.add_parser('mem', help='Memory forensics analysis')
    mem_parser.add_argument('--info', action='store_true', 
                           help='Show memory information')
    mem_parser.add_argument('--list-procs', action='store_true', 
                           help='List processes with memory info')
    mem_parser.add_argument('--memory-map', action='store_true', 
                           help='Get memory map for process')
    mem_parser.add_argument('--dump', action='store_true', 
                           help='Dump process memory')
    mem_parser.add_argument('--scan-strings', action='store_true', 
                           help='Scan memory for strings')
    mem_parser.add_argument('--anomalies', action='store_true', 
                           help='Detect memory anomalies')
    mem_parser.add_argument('--stats', action='store_true', 
                           help='Get memory statistics')
    mem_parser.add_argument('--pid', type=int, 
                           help='Process ID for specific operations')
    mem_parser.add_argument('--output', type=str, 
                           help='Output file for memory dump')
    mem_parser.add_argument('--strings', type=str, 
                           help='Comma-separated strings to search for')
    mem_parser.add_argument('--limit', type=int, default=20, 
                           help='Limit number of processes to show')
    mem_parser.add_argument('--export', type=str, 
                           help='Export memory analysis to file')
    mem_parser.add_argument('--export-format', choices=['json', 'csv', 'txt'], 
                           default='json', help='Export format')
    mem_parser.add_argument('--compress', action='store_true', 
                           help='Compress exported file')
    
    # SIEM subcommand
    siem_parser = subparsers.add_parser('siem', help='SIEM API integration')
    siem_parser.add_argument('--type', choices=['elk', 'wazuh', 'splunk'], 
                           required=True, help='SIEM type')
    siem_parser.add_argument('--host', type=str, required=True, 
                           help='SIEM host address')
    siem_parser.add_argument('--port', type=int, 
                           help='SIEM port (defaults based on type)')
    siem_parser.add_argument('--username', type=str, 
                           help='Username for authentication')
    siem_parser.add_argument('--password', type=str, 
                           help='Password for authentication')
    siem_parser.add_argument('--api-key', type=str, 
                           help='API key for authentication')
    siem_parser.add_argument('--alerts', action='store_true', 
                           help='Get recent alerts')
    siem_parser.add_argument('--search', type=str, 
                           help='Search for specific alerts')
    siem_parser.add_argument('--query', type=str, 
                           help='Run custom query')
    siem_parser.add_argument('--limit', type=int, default=100, 
                           help='Limit number of results')
    siem_parser.add_argument('--time-range', type=str, default='24h', 
                           help='Time range for queries (e.g., 24h, 7d)')
    siem_parser.add_argument('--export', type=str, 
                           help='Export SIEM results to file')
    siem_parser.add_argument('--export-format', choices=['json', 'csv', 'txt'], 
                           default='json', help='Export format')
    siem_parser.add_argument('--compress', action='store_true', 
                           help='Compress exported file')
    
    # Automation subcommand
    automation_parser = subparsers.add_parser('automation', help='Automation scheduling')
    automation_parser.add_argument('--add', action='store_true', 
                                 help='Add new scheduled task')
    automation_parser.add_argument('--remove', action='store_true', 
                                 help='Remove scheduled task')
    automation_parser.add_argument('--enable', action='store_true', 
                                 help='Enable scheduled task')
    automation_parser.add_argument('--disable', action='store_true', 
                                 help='Disable scheduled task')
    automation_parser.add_argument('--list', action='store_true', 
                                 help='List scheduled tasks')
    automation_parser.add_argument('--execute', action='store_true', 
                                 help='Execute task immediately')
    automation_parser.add_argument('--start', action='store_true', 
                                 help='Start task scheduler')
    automation_parser.add_argument('--system-task', action='store_true', 
                                 help='Create system task (cron/schtasks)')
    automation_parser.add_argument('--execute-system', action='store_true', 
                                 help='Execute system task command')
    automation_parser.add_argument('--task-id', type=str, 
                                 help='Task ID')
    automation_parser.add_argument('--task-type', choices=['hunt', 'logs', 'ir', 'mem', 'net'], 
                                 help='Task type')
    automation_parser.add_argument('--schedule-type', choices=['daily', 'weekly', 'hourly', 'custom'], 
                                 help='Schedule type')
    automation_parser.add_argument('--schedule-value', type=str, 
                                 help='Schedule value (e.g., "14:30", "monday", "2h")')
    automation_parser.add_argument('--command', type=str, 
                                 help='Custom command to execute')
    automation_parser.add_argument('--enabled', action='store_true', default=True, 
                                 help='Enable task (default: True)')
    
    # Alerts subcommand
    alerts_parser = subparsers.add_parser('alerts', help='Alerting notifications')
    alerts_parser.add_argument('--configure', action='store_true', 
                             help='Configure alerting system')
    alerts_parser.add_argument('--channel', choices=['slack', 'teams', 'email'], 
                             help='Channel to configure')
    alerts_parser.add_argument('--enable', action='store_true', 
                             help='Enable alerting system')
    alerts_parser.add_argument('--disable', action='store_true', 
                             help='Disable alerting system')
    alerts_parser.add_argument('--test', action='store_true', 
                             help='Send test alert')
    alerts_parser.add_argument('--message', type=str, 
                             help='Test message')
    alerts_parser.add_argument('--severity', choices=['low', 'medium', 'high'], 
                             help='Alert severity')
    alerts_parser.add_argument('--subject', type=str, 
                             help='Alert subject')
    alerts_parser.add_argument('--config', action='store_true', 
                             help='Show alerting configuration')
    
    # Logs subcommand
    logs_parser = subparsers.add_parser('logs', help='Collect and filter system logs')
    logs_parser.add_argument('--os', choices=['windows', 'linux'], 
                           default='windows', help='Target operating system')
    logs_parser.add_argument('--lines', type=int, default=50, 
                           help='Number of log lines to retrieve')
    logs_parser.add_argument('--filter', type=str, 
                           help='Filter logs by keyword')
    logs_parser.add_argument('--export', type=str, 
                           help='Export logs to file (JSON/CSV/TXT)')
    logs_parser.add_argument('--export-format', choices=['json', 'csv', 'txt'], 
                           default='json', help='Export format')
    logs_parser.add_argument('--compress', action='store_true', 
                           help='Compress exported file')
    
    # Hunt subcommand
    hunt_parser = subparsers.add_parser('hunt', help='Threat hunting based on MITRE ATT&CK and Sigma rules')
    hunt_parser.add_argument('--technique', type=str, 
                           help='MITRE ATT&CK technique ID (e.g., T1053)')
    hunt_parser.add_argument('--sigma', type=str, 
                           help='Path to Sigma rule file or directory')
    hunt_parser.add_argument('--list', action='store_true', 
                           help='List available hunting techniques')
    hunt_parser.add_argument('--verbose', action='store_true', 
                           help='Verbose output')
    hunt_parser.add_argument('--export', type=str, 
                           help='Export hunt results to file')
    hunt_parser.add_argument('--export-format', choices=['json', 'csv', 'txt'], 
                           default='json', help='Export format')
    hunt_parser.add_argument('--compress', action='store_true', 
                           help='Compress exported file')
    
    # IR subcommand
    ir_parser = subparsers.add_parser('ir', help='Incident response snapshot and containment')
    ir_parser.add_argument('--quarantine', action='store_true', 
                          help='Quarantine suspicious files')
    ir_parser.add_argument('--block-ip', type=str, 
                          help='Block specific IP address')
    ir_parser.add_argument('--block-duration', type=int, default=3600,
                          help='IP block duration in seconds (default: 3600)')
    ir_parser.add_argument('--kill-process', type=int, 
                          help='Kill process by PID')
    ir_parser.add_argument('--force-kill', action='store_true',
                          help='Force kill process (use with --kill-process)')
    ir_parser.add_argument('--suspend-process', type=int, 
                          help='Suspend process by PID')
    ir_parser.add_argument('--list-quarantined', action='store_true',
                          help='List quarantined files')
    ir_parser.add_argument('--restore-file', type=str, 
                          help='Restore quarantined file')
    ir_parser.add_argument('--restore-path', type=str, 
                          help='Path to restore file to (use with --restore-file)')
    ir_parser.add_argument('--output', type=str, default='ir_report.json',
                          help='Output file for IR report')
    ir_parser.add_argument('--export-format', choices=['json', 'csv', 'txt'], 
                          default='json', help='Export format')
    ir_parser.add_argument('--compress', action='store_true', 
                          help='Compress exported file')
    ir_parser.add_argument('--include-memory', action='store_true',
                          help='Include memory analysis (if available)')
    
    # IOC subcommand
    ioc_parser = subparsers.add_parser('ioc', help='IOC scanning and enrichment')
    ioc_parser.add_argument('--type', choices=['ip', 'domain', 'hash'], 
                           required=True, help='Type of IOC')
    ioc_parser.add_argument('--value', type=str, required=True, 
                           help='IOC value to scan')
    ioc_parser.add_argument('--vt', action='store_true', 
                           help='Enrich with VirusTotal')
    ioc_parser.add_argument('--scan-logs', action='store_true', 
                           help='Scan system logs for IOC')
    ioc_parser.add_argument('--scan-processes', action='store_true', 
                           help='Scan running processes for IOC')
    ioc_parser.add_argument('--export', type=str, 
                           help='Export IOC scan results to file')
    ioc_parser.add_argument('--export-format', choices=['json', 'csv', 'txt'], 
                           default='json', help='Export format')
    ioc_parser.add_argument('--compress', action='store_true', 
                           help='Compress exported file')
    
    # Network subcommand
    net_parser = subparsers.add_parser('net', help='Network defense utilities')
    net_parser.add_argument('--connections', action='store_true', 
                           help='Show active network connections')
    net_parser.add_argument('--beaconing', action='store_true', 
                           help='Detect beaconing patterns')
    net_parser.add_argument('--block', type=str, 
                           help='Block IP address (requires admin)')
    net_parser.add_argument('--dns-cache', action='store_true', 
                           help='Show DNS cache entries')
    net_parser.add_argument('--export', type=str, 
                           help='Export network analysis to file')
    net_parser.add_argument('--export-format', choices=['json', 'csv', 'txt'], 
                           default='json', help='Export format')
    net_parser.add_argument('--compress', action='store_true', 
                           help='Compress exported file')
    
    return parser


def main():
    """Main entry point for the Blue Team CLI Toolkit."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Dispatch to appropriate module
        if args.command == 'logs':
            logs.main(args)
        elif args.command == 'hunt':
            hunt.main(args)
        elif args.command == 'ir':
            ir.main(args)
        elif args.command == 'ioc':
            ioc.main(args)
        elif args.command == 'net':
            net.main(args)
        elif args.command == 'mem':
            mem.main(args)
        elif args.command == 'siem':
            siem.main(args)
        elif args.command == 'automation':
            automation.main(args)
        elif args.command == 'alerts':
            alerts.main(args)
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error: {e}")
        if utils.DEBUG_MODE:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
