"""
Alerting Notifications Module for the Blue Team CLI Toolkit.
Provides capabilities for sending alerts via Slack, Teams, email, and other channels.
"""

import os
import sys
import platform
import subprocess
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional
from datetime import datetime
import utils


class AlertManager:
    """Alert manager for sending notifications."""
    
    def __init__(self, config_file: str = "alerts_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.alert_history = []
    
    def load_config(self) -> Dict[str, Any]:
        """Load alerting configuration from file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    utils.print_info(f"Loaded alerting configuration")
                    return config
            else:
                # Create default configuration
                default_config = {
                    'enabled': False,
                    'channels': {
                        'slack': {'enabled': False, 'webhook_url': '', 'channel': '#alerts'},
                        'teams': {'enabled': False, 'webhook_url': ''},
                        'email': {
                            'enabled': False, 'smtp_server': '', 'smtp_port': 587,
                            'username': '', 'password': '', 'from_email': '', 'to_emails': []
                        }
                    },
                    'rules': {
                        'failed_logins': {'enabled': True, 'threshold': 5, 'time_window': 300},
                        'suspicious_processes': {'enabled': True, 'threshold': 1},
                        'network_anomalies': {'enabled': True, 'threshold': 3},
                        'file_quarantine': {'enabled': True, 'threshold': 1}
                    },
                    'last_updated': datetime.now().isoformat()
                }
                self.save_config(default_config)
                return default_config
        except Exception as e:
            utils.print_error(f"Failed to load alerting config: {e}")
            return {'enabled': False, 'channels': {}, 'rules': {}}
    
    def save_config(self, config: Dict[str, Any] = None):
        """Save alerting configuration to file."""
        try:
            if config is None:
                config = self.config
            config['last_updated'] = datetime.now().isoformat()
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            utils.print_error(f"Failed to save alerting config: {e}")
    
    def send_slack_alert(self, message: str, severity: str = "medium") -> bool:
        """Send alert to Slack."""
        try:
            slack_config = self.config.get('channels', {}).get('slack', {})
            if not slack_config.get('enabled', False):
                return False
            
            webhook_url = slack_config.get('webhook_url', '')
            channel = slack_config.get('channel', '#alerts')
            
            if not webhook_url:
                utils.print_error("Slack webhook URL not configured")
                return False
            
            color_map = {'low': '#36a64f', 'medium': '#ff8c00', 'high': '#ff0000'}
            
            payload = {
                'channel': channel,
                'attachments': [{
                    'color': color_map.get(severity, '#36a64f'),
                    'title': f"Blue Team Alert - {severity.upper()}",
                    'text': message,
                    'footer': 'Blue Team CLI Toolkit',
                    'ts': int(datetime.now().timestamp())
                }]
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                utils.print_success("Slack alert sent successfully")
                return True
            else:
                utils.print_error(f"Failed to send Slack alert: {response.status_code}")
                return False
                
        except Exception as e:
            utils.print_error(f"Failed to send Slack alert: {e}")
            return False
    
    def send_teams_alert(self, message: str, severity: str = "medium") -> bool:
        """Send alert to Microsoft Teams."""
        try:
            teams_config = self.config.get('channels', {}).get('teams', {})
            if not teams_config.get('enabled', False):
                return False
            
            webhook_url = teams_config.get('webhook_url', '')
            
            if not webhook_url:
                utils.print_error("Teams webhook URL not configured")
                return False
            
            color_map = {'low': '00FF00', 'medium': 'FF8C00', 'high': 'FF0000'}
            
            payload = {
                '@type': 'MessageCard',
                '@context': 'http://schema.org/extensions',
                'themeColor': color_map.get(severity, '00FF00'),
                'summary': f"Blue Team Alert - {severity.upper()}",
                'sections': [{
                    'activityTitle': f"Blue Team Alert - {severity.upper()}",
                    'activitySubtitle': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'text': message,
                    'markdown': True
                }]
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                utils.print_success("Teams alert sent successfully")
                return True
            else:
                utils.print_error(f"Failed to send Teams alert: {response.status_code}")
                return False
                
        except Exception as e:
            utils.print_error(f"Failed to send Teams alert: {e}")
            return False
    
    def send_email_alert(self, subject: str, message: str, severity: str = "medium") -> bool:
        """Send alert via email."""
        try:
            email_config = self.config.get('channels', {}).get('email', {})
            if not email_config.get('enabled', False):
                return False
            
            smtp_server = email_config.get('smtp_server', '')
            smtp_port = email_config.get('smtp_port', 587)
            username = email_config.get('username', '')
            password = email_config.get('password', '')
            from_email = email_config.get('from_email', '')
            to_emails = email_config.get('to_emails', [])
            
            if not all([smtp_server, username, password, from_email, to_emails]):
                utils.print_error("Email configuration incomplete")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = f"[{severity.upper()}] {subject}"
            
            severity_indicators = {'low': '🟢', 'medium': '🟠', 'high': '🔴'}
            
            formatted_message = f"""
{severity_indicators.get(severity, '🟢')} Blue Team Alert - {severity.upper()}

{message}

---
Generated by Blue Team CLI Toolkit
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            msg.attach(MIMEText(formatted_message, 'plain'))
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            
            utils.print_success("Email alert sent successfully")
            return True
            
        except Exception as e:
            utils.print_error(f"Failed to send email alert: {e}")
            return False
    
    def send_alert(self, message: str, severity: str = "medium", subject: str = None) -> bool:
        """Send alert to all configured channels."""
        if not self.config.get('enabled', False):
            utils.print_info("Alerting is disabled")
            return False
        
        success = False
        
        if self.config.get('channels', {}).get('slack', {}).get('enabled', False):
            if self.send_slack_alert(message, severity):
                success = True
        
        if self.config.get('channels', {}).get('teams', {}).get('enabled', False):
            if self.send_teams_alert(message, severity):
                success = True
        
        if self.config.get('channels', {}).get('email', {}).get('enabled', False):
            if self.send_email_alert(subject or f"Blue Team Alert - {severity.upper()}", message, severity):
                success = True
        
        alert_entry = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'severity': severity,
            'subject': subject,
            'sent': success
        }
        self.alert_history.append(alert_entry)
        
        return success
    
    def configure_channel(self, channel: str, enabled: bool = True, **kwargs) -> bool:
        """Configure a notification channel."""
        try:
            if 'channels' not in self.config:
                self.config['channels'] = {}
            
            if channel not in self.config['channels']:
                self.config['channels'][channel] = {}
            
            self.config['channels'][channel]['enabled'] = enabled
            
            for key, value in kwargs.items():
                self.config['channels'][channel][key] = value
            
            self.save_config()
            utils.print_success(f"Configured {channel} channel")
            return True
            
        except Exception as e:
            utils.print_error(f"Failed to configure {channel} channel: {e}")
            return False
    
    def enable_alerting(self) -> bool:
        """Enable alerting system."""
        try:
            self.config['enabled'] = True
            self.save_config()
            utils.print_success("Alerting system enabled")
            return True
        except Exception as e:
            utils.print_error(f"Failed to enable alerting: {e}")
            return False
    
    def disable_alerting(self) -> bool:
        """Disable alerting system."""
        try:
            self.config['enabled'] = False
            self.save_config()
            utils.print_success("Alerting system disabled")
            return True
        except Exception as e:
            utils.print_error(f"Failed to disable alerting: {e}")
            return False


def display_config(config: Dict[str, Any]):
    """Display alerting configuration."""
    utils.print_section("Alerting Configuration")
    
    status = "✅ Enabled" if config.get('enabled', False) else "❌ Disabled"
    print(f"Alerting System: {status}")
    
    utils.print_section("Notification Channels")
    channels = config.get('channels', {})
    
    for channel_name, channel_config in channels.items():
        status = "✅ Enabled" if channel_config.get('enabled', False) else "❌ Disabled"
        print(f"\n{channel_name.title()}: {status}")
        
        if channel_name == 'slack':
            webhook = channel_config.get('webhook_url', 'Not configured')
            channel = channel_config.get('channel', '#alerts')
            print(f"  Webhook: {webhook[:50]}..." if len(webhook) > 50 else f"  Webhook: {webhook}")
            print(f"  Channel: {channel}")
        elif channel_name == 'teams':
            webhook = channel_config.get('webhook_url', 'Not configured')
            print(f"  Webhook: {webhook[:50]}..." if len(webhook) > 50 else f"  Webhook: {webhook}")
        elif channel_name == 'email':
            smtp_server = channel_config.get('smtp_server', 'Not configured')
            from_email = channel_config.get('from_email', 'Not configured')
            to_emails = channel_config.get('to_emails', [])
            print(f"  SMTP Server: {smtp_server}")
            print(f"  From: {from_email}")
            print(f"  To: {', '.join(to_emails) if to_emails else 'Not configured'}")


def main(args):
    """Main function for alerting notifications module."""
    utils.print_banner()
    utils.print_section("Alerting Notifications")
    
    alert_manager = AlertManager()
    
    try:
        if args.configure:
            # Configure alerting system
            if args.channel:
                if args.channel == 'slack':
                    webhook_url = input("Enter Slack webhook URL: ").strip()
                    channel = input("Enter Slack channel (default: #alerts): ").strip() or "#alerts"
                    alert_manager.configure_channel('slack', True, webhook_url=webhook_url, channel=channel)
                
                elif args.channel == 'teams':
                    webhook_url = input("Enter Teams webhook URL: ").strip()
                    alert_manager.configure_channel('teams', True, webhook_url=webhook_url)
                
                elif args.channel == 'email':
                    smtp_server = input("Enter SMTP server: ").strip()
                    smtp_port = int(input("Enter SMTP port (default: 587): ").strip() or "587")
                    username = input("Enter email username: ").strip()
                    password = input("Enter email password: ").strip()
                    from_email = input("Enter from email: ").strip()
                    to_emails = input("Enter to emails (comma-separated): ").strip().split(',')
                    
                    alert_manager.configure_channel('email', True, 
                                                  smtp_server=smtp_server,
                                                  smtp_port=smtp_port,
                                                  username=username,
                                                  password=password,
                                                  from_email=from_email,
                                                  to_emails=to_emails)
        
        elif args.enable:
            alert_manager.enable_alerting()
        
        elif args.disable:
            alert_manager.disable_alerting()
        
        elif args.test:
            message = args.message or "This is a test alert from Blue Team CLI Toolkit"
            severity = args.severity or "medium"
            subject = args.subject or "Test Alert"
            
            utils.print_info(f"Sending test alert: {message}")
            if alert_manager.send_alert(message, severity, subject):
                utils.print_success("Test alert sent successfully")
            else:
                utils.print_error("Test alert failed")
        
        elif args.config:
            display_config(alert_manager.config)
        
        else:
            utils.print_error("No action specified. Use --help for usage information.")
    
    except Exception as e:
        utils.print_error(f"Alerting failed: {e}")


if __name__ == "__main__":
    # For testing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--configure', action='store_true', help='Configure alerting')
    parser.add_argument('--channel', choices=['slack', 'teams', 'email'], help='Channel to configure')
    parser.add_argument('--enable', action='store_true', help='Enable alerting')
    parser.add_argument('--disable', action='store_true', help='Disable alerting')
    parser.add_argument('--test', action='store_true', help='Send test alert')
    parser.add_argument('--message', type=str, help='Test message')
    parser.add_argument('--severity', choices=['low', 'medium', 'high'], help='Alert severity')
    parser.add_argument('--subject', type=str, help='Alert subject')
    parser.add_argument('--config', action='store_true', help='Show configuration')
    args = parser.parse_args()
    main(args)
