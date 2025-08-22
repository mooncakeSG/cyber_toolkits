"""
Automation Scheduling Module for the Blue Team CLI Toolkit.
Provides capabilities for scheduling automated tasks and generating periodic reports.
"""

import os
import sys
import platform
import subprocess
import json
import schedule
import time
import threading
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
import utils


class TaskScheduler:
    """Task scheduler for automated operations."""
    
    def __init__(self):
        self.tasks = {}
        self.scheduler_thread = None
        self.running = False
        self.config_file = "automation_config.json"
        self.load_config()
    
    def load_config(self):
        """Load automation configuration from file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.tasks = config.get('tasks', {})
                    utils.print_info(f"Loaded {len(self.tasks)} scheduled tasks")
            else:
                self.tasks = {}
        except Exception as e:
            utils.print_error(f"Failed to load automation config: {e}")
            self.tasks = {}
    
    def save_config(self):
        """Save automation configuration to file."""
        try:
            config = {
                'tasks': self.tasks,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            utils.print_error(f"Failed to save automation config: {e}")
    
    def add_task(self, task_id: str, task_type: str, schedule_type: str, 
                 schedule_value: str, command: str, enabled: bool = True) -> bool:
        """
        Add a new scheduled task.
        
        Args:
            task_id: Unique identifier for the task
            task_type: Type of task (hunt, logs, ir, mem, net)
            schedule_type: Schedule type (daily, weekly, hourly, custom)
            schedule_value: Schedule value (e.g., "14:30", "monday", "2h")
            command: Command to execute
            enabled: Whether the task is enabled
            
        Returns:
            True if successful, False otherwise
        """
        try:
            task = {
                'id': task_id,
                'type': task_type,
                'schedule_type': schedule_type,
                'schedule_value': schedule_value,
                'command': command,
                'enabled': enabled,
                'created': datetime.now().isoformat(),
                'last_run': None,
                'next_run': None,
                'run_count': 0,
                'last_status': None
            }
            
            self.tasks[task_id] = task
            self.save_config()
            utils.print_success(f"Added task: {task_id}")
            return True
            
        except Exception as e:
            utils.print_error(f"Failed to add task: {e}")
            return False
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a scheduled task."""
        try:
            if task_id in self.tasks:
                del self.tasks[task_id]
                self.save_config()
                utils.print_success(f"Removed task: {task_id}")
                return True
            else:
                utils.print_error(f"Task not found: {task_id}")
                return False
        except Exception as e:
            utils.print_error(f"Failed to remove task: {e}")
            return False
    
    def enable_task(self, task_id: str) -> bool:
        """Enable a scheduled task."""
        try:
            if task_id in self.tasks:
                self.tasks[task_id]['enabled'] = True
                self.save_config()
                utils.print_success(f"Enabled task: {task_id}")
                return True
            else:
                utils.print_error(f"Task not found: {task_id}")
                return False
        except Exception as e:
            utils.print_error(f"Failed to enable task: {e}")
            return False
    
    def disable_task(self, task_id: str) -> bool:
        """Disable a scheduled task."""
        try:
            if task_id in self.tasks:
                self.tasks[task_id]['enabled'] = False
                self.save_config()
                utils.print_success(f"Disabled task: {task_id}")
                return True
            else:
                utils.print_error(f"Task not found: {task_id}")
                return False
        except Exception as e:
            utils.print_error(f"Failed to disable task: {e}")
            return False
    
    def list_tasks(self) -> List[Dict]:
        """List all scheduled tasks."""
        return list(self.tasks.values())
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get a specific task by ID."""
        return self.tasks.get(task_id)
    
    def execute_task(self, task: Dict) -> bool:
        """Execute a scheduled task."""
        try:
            task_id = task['id']
            task_type = task['type']
            command = task['command']
            
            utils.print_info(f"Executing task: {task_id} ({task_type})")
            
            # Update task status
            task['last_run'] = datetime.now().isoformat()
            task['run_count'] += 1
            
            # Execute the command
            if platform.system() == "Windows":
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
            else:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                task['last_status'] = 'success'
                utils.print_success(f"Task {task_id} completed successfully")
                
                # Generate report if needed
                if task_type in ['hunt', 'ir', 'mem']:
                    self.generate_automated_report(task)
                
                return True
            else:
                task['last_status'] = 'failed'
                utils.print_error(f"Task {task_id} failed: {result.stderr}")
                return False
                
        except Exception as e:
            task['last_status'] = 'error'
            utils.print_error(f"Task {task_id} error: {e}")
            return False
        finally:
            self.save_config()
    
    def generate_automated_report(self, task: Dict):
        """Generate automated report for completed task."""
        try:
            task_id = task['id']
            task_type = task['type']
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create reports directory
            reports_dir = "automated_reports"
            os.makedirs(reports_dir, exist_ok=True)
            
            # Generate report filename
            report_filename = f"{reports_dir}/{task_type}_report_{timestamp}.json"
            
            # Create report content
            report = {
                'task_id': task_id,
                'task_type': task_type,
                'execution_time': task['last_run'],
                'status': task['last_status'],
                'run_count': task['run_count'],
                'command': task['command'],
                'report_generated': timestamp
            }
            
            # Save report
            with open(report_filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            utils.print_info(f"Generated automated report: {report_filename}")
            
        except Exception as e:
            utils.print_error(f"Failed to generate automated report: {e}")
    
    def setup_schedule(self):
        """Setup the schedule for all enabled tasks."""
        try:
            schedule.clear()
            
            for task_id, task in self.tasks.items():
                if not task.get('enabled', True):
                    continue
                
                schedule_type = task['schedule_type']
                schedule_value = task['schedule_value']
                
                # Create task execution function
                def create_task_executor(task_dict):
                    return lambda: self.execute_task(task_dict)
                
                task_executor = create_task_executor(task)
                
                # Schedule based on type
                if schedule_type == 'daily':
                    schedule.every().day.at(schedule_value).do(task_executor)
                elif schedule_type == 'weekly':
                    schedule.every().monday.at(schedule_value).do(task_executor)
                elif schedule_type == 'hourly':
                    schedule.every(int(schedule_value)).hours.do(task_executor)
                elif schedule_type == 'custom':
                    # Parse custom schedule (e.g., "2h", "30m", "1d")
                    if schedule_value.endswith('h'):
                        hours = int(schedule_value[:-1])
                        schedule.every(hours).hours.do(task_executor)
                    elif schedule_value.endswith('m'):
                        minutes = int(schedule_value[:-1])
                        schedule.every(minutes).minutes.do(task_executor)
                    elif schedule_value.endswith('d'):
                        days = int(schedule_value[:-1])
                        schedule.every(days).days.do(task_executor)
                
                utils.print_info(f"Scheduled task: {task_id} ({schedule_type}: {schedule_value})")
            
            utils.print_success(f"Setup {len([t for t in self.tasks.values() if t.get('enabled', True)])} scheduled tasks")
            
        except Exception as e:
            utils.print_error(f"Failed to setup schedule: {e}")
    
    def start_scheduler(self):
        """Start the task scheduler."""
        try:
            if self.running:
                utils.print_warning("Scheduler is already running")
                return
            
            self.setup_schedule()
            self.running = True
            
            def run_scheduler():
                while self.running:
                    schedule.run_pending()
                    time.sleep(60)  # Check every minute
            
            self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            self.scheduler_thread.start()
            
            utils.print_success("Task scheduler started")
            
        except Exception as e:
            utils.print_error(f"Failed to start scheduler: {e}")
    
    def stop_scheduler(self):
        """Stop the task scheduler."""
        try:
            self.running = False
            if self.scheduler_thread:
                self.scheduler_thread.join(timeout=5)
            utils.print_success("Task scheduler stopped")
        except Exception as e:
            utils.print_error(f"Failed to stop scheduler: {e}")


def create_system_task(task_type: str, schedule_type: str, schedule_value: str) -> str:
    """
    Create a system task using platform-specific tools.
    
    Args:
        task_type: Type of task (hunt, logs, ir, mem, net)
        schedule_type: Schedule type (daily, weekly, hourly)
        schedule_value: Schedule value
        
    Returns:
        Command string for the task
    """
    base_command = f"python main.py {task_type}"
    
    if platform.system() == "Windows":
        # Windows Task Scheduler
        task_name = f"BlueTeam_{task_type}_{schedule_type}"
        
        if schedule_type == "daily":
            schedule_cmd = f"/sc daily /st {schedule_value}"
        elif schedule_type == "weekly":
            schedule_cmd = f"/sc weekly /d {schedule_value}"
        elif schedule_type == "hourly":
            schedule_cmd = f"/sc minute /mo {schedule_value}"
        else:
            schedule_cmd = f"/sc daily /st {schedule_value}"
        
        command = f'schtasks /create /tn "{task_name}" /tr "{base_command}" {schedule_cmd} /ru System'
        
    else:
        # Linux cron
        if schedule_type == "daily":
            hour, minute = schedule_value.split(":")
            cron_schedule = f"{minute} {hour} * * *"
        elif schedule_type == "weekly":
            hour, minute = schedule_value.split(":")
            day_map = {"monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, 
                      "friday": 5, "saturday": 6, "sunday": 0}
            day = day_map.get(schedule_value.lower(), 1)
            cron_schedule = f"{minute} {hour} * * {day}"
        elif schedule_type == "hourly":
            cron_schedule = f"0 */{schedule_value} * * *"
        else:
            cron_schedule = "0 0 * * *"  # Daily at midnight
        
        command = f'(crontab -l 2>/dev/null; echo "{cron_schedule} cd {os.getcwd()} && {base_command}") | crontab -'
    
    return command


def display_tasks(tasks: List[Dict]):
    """Display scheduled tasks."""
    if not tasks:
        utils.print_info("No scheduled tasks found")
        return
    
    utils.print_section(f"Scheduled Tasks: {len(tasks)}")
    
    for i, task in enumerate(tasks, 1):
        status = "✅ Enabled" if task.get('enabled', True) else "❌ Disabled"
        last_run = task.get('last_run', 'Never')
        last_status = task.get('last_status', 'Unknown')
        
        print(f"\n{i}. {task['id']} ({task['type']}) - {status}")
        print(f"   Schedule: {task['schedule_type']} at {task['schedule_value']}")
        print(f"   Command: {task['command']}")
        print(f"   Last Run: {last_run}")
        print(f"   Last Status: {last_status}")
        print(f"   Run Count: {task.get('run_count', 0)}")


def main(args):
    """Main function for automation scheduling module."""
    utils.print_banner()
    utils.print_section("Automation Scheduling")
    
    scheduler = TaskScheduler()
    
    try:
        if args.add:
            # Add new task
            task_id = args.task_id or f"{args.task_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            command = args.command or f"python main.py {args.task_type}"
            
            if scheduler.add_task(task_id, args.task_type, args.schedule_type, 
                                args.schedule_value, command, args.enabled):
                utils.print_success(f"Task added successfully: {task_id}")
            else:
                utils.print_error("Failed to add task")
        
        elif args.remove:
            # Remove task
            if scheduler.remove_task(args.task_id):
                utils.print_success("Task removed successfully")
            else:
                utils.print_error("Failed to remove task")
        
        elif args.enable:
            # Enable task
            if scheduler.enable_task(args.task_id):
                utils.print_success("Task enabled successfully")
            else:
                utils.print_error("Failed to enable task")
        
        elif args.disable:
            # Disable task
            if scheduler.disable_task(args.task_id):
                utils.print_success("Task disabled successfully")
            else:
                utils.print_error("Failed to disable task")
        
        elif args.list:
            # List tasks
            tasks = scheduler.list_tasks()
            display_tasks(tasks)
        
        elif args.execute:
            # Execute task immediately
            task = scheduler.get_task(args.task_id)
            if task:
                if scheduler.execute_task(task):
                    utils.print_success("Task executed successfully")
                else:
                    utils.print_error("Task execution failed")
            else:
                utils.print_error(f"Task not found: {args.task_id}")
        
        elif args.start:
            # Start scheduler
            scheduler.start_scheduler()
            utils.print_info("Scheduler started. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                scheduler.stop_scheduler()
        
        elif args.system_task:
            # Create system task
            command = create_system_task(args.task_type, args.schedule_type, args.schedule_value)
            utils.print_info(f"System task command:")
            print(f"  {command}")
            
            if args.execute_system:
                utils.print_warning("Executing system task command (requires admin privileges)...")
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    utils.print_success("System task created successfully")
                else:
                    utils.print_error(f"Failed to create system task: {result.stderr}")
        
        else:
            utils.print_error("No action specified. Use --help for usage information.")
    
    except Exception as e:
        utils.print_error(f"Automation scheduling failed: {e}")


if __name__ == "__main__":
    # For testing
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--add', action='store_true', help='Add new task')
    parser.add_argument('--remove', action='store_true', help='Remove task')
    parser.add_argument('--enable', action='store_true', help='Enable task')
    parser.add_argument('--disable', action='store_true', help='Disable task')
    parser.add_argument('--list', action='store_true', help='List tasks')
    parser.add_argument('--execute', action='store_true', help='Execute task')
    parser.add_argument('--start', action='store_true', help='Start scheduler')
    parser.add_argument('--system-task', action='store_true', help='Create system task')
    parser.add_argument('--execute-system', action='store_true', help='Execute system task command')
    parser.add_argument('--task-id', type=str, help='Task ID')
    parser.add_argument('--task-type', choices=['hunt', 'logs', 'ir', 'mem', 'net'], help='Task type')
    parser.add_argument('--schedule-type', choices=['daily', 'weekly', 'hourly', 'custom'], help='Schedule type')
    parser.add_argument('--schedule-value', type=str, help='Schedule value')
    parser.add_argument('--command', type=str, help='Command to execute')
    parser.add_argument('--enabled', action='store_true', default=True, help='Enable task')
    args = parser.parse_args()
    main(args)
