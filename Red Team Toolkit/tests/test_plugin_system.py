#!/usr/bin/env python3
"""
Test suite for the plugin system functionality.
"""

import unittest
import tempfile
import shutil
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the main toolkit
sys.path.insert(0, str(Path(__file__).parent.parent))

from red_team_toolkit import PluginManager, TaskScheduler, SandboxMode

class TestPluginManager(unittest.TestCase):
    """Test cases for the PluginManager class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.plugin_manager = PluginManager()
        self.plugin_manager.plugins_dir = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_discover_plugins_empty_directory(self):
        """Test plugin discovery in empty directory."""
        plugins = self.plugin_manager.discover_plugins()
        self.assertEqual(plugins, [])
    
    def test_discover_plugins_with_files(self):
        """Test plugin discovery with Python files."""
        # Create test plugin files
        plugin1 = Path(self.temp_dir) / "test_plugin1.py"
        plugin2 = Path(self.temp_dir) / "test_plugin2.py"
        private_file = Path(self.temp_dir) / "_private.py"
        
        plugin1.write_text("# Test plugin 1")
        plugin2.write_text("# Test plugin 2")
        private_file.write_text("# Private file")
        
        plugins = self.plugin_manager.discover_plugins()
        self.assertEqual(len(plugins), 2)
        self.assertIn("test_plugin1", plugins)
        self.assertIn("test_plugin2", plugins)
        self.assertNotIn("_private", plugins)
    
    def test_load_plugin_success(self):
        """Test successful plugin loading."""
        plugin_content = '''
__version__ = "1.0.0"
__description__ = "Test plugin"
__author__ = "Test Author"
__requires_sandbox__ = True
__category__ = "Test"

def test_function():
    return "Hello from plugin"
'''
        plugin_file = Path(self.temp_dir) / "test_plugin.py"
        plugin_file.write_text(plugin_content)
        
        success = self.plugin_manager.load_plugin("test_plugin")
        self.assertTrue(success)
        self.assertIn("test_plugin", self.plugin_manager.loaded_plugins)
        
        # Test function execution
        result = self.plugin_manager.execute_plugin_function("test_plugin", "test_function")
        self.assertEqual(result, "Hello from plugin")
    
    def test_load_plugin_file_not_found(self):
        """Test plugin loading with non-existent file."""
        success = self.plugin_manager.load_plugin("nonexistent_plugin")
        self.assertFalse(success)
    
    def test_extract_plugin_metadata(self):
        """Test plugin metadata extraction."""
        plugin_content = '''
__version__ = "2.0.0"
__description__ = "Advanced test plugin"
__author__ = "Advanced Author"
__requires_sandbox__ = False
__category__ = "Advanced"

def function1():
    pass

def function2():
    pass
'''
        plugin_file = Path(self.temp_dir) / "advanced_plugin.py"
        plugin_file.write_text(plugin_content)
        
        # Load plugin to extract metadata
        self.plugin_manager.load_plugin("advanced_plugin")
        metadata = self.plugin_manager.get_plugin_info("advanced_plugin")
        
        self.assertEqual(metadata['version'], "2.0.0")
        self.assertEqual(metadata['description'], "Advanced test plugin")
        self.assertEqual(metadata['author'], "Advanced Author")
        self.assertFalse(metadata['requires_sandbox'])
        self.assertEqual(metadata['category'], "Advanced")
        self.assertIn('function1', metadata['functions'])
        self.assertIn('function2', metadata['functions'])
    
    def test_unload_plugin(self):
        """Test plugin unloading."""
        plugin_content = '''
def test_function():
    return "test"
'''
        plugin_file = Path(self.temp_dir) / "test_plugin.py"
        plugin_file.write_text(plugin_content)
        
        # Load and then unload plugin
        self.plugin_manager.load_plugin("test_plugin")
        self.assertIn("test_plugin", self.plugin_manager.loaded_plugins)
        
        success = self.plugin_manager.unload_plugin("test_plugin")
        self.assertTrue(success)
        self.assertNotIn("test_plugin", self.plugin_manager.loaded_plugins)
    
    def test_execute_plugin_function_not_loaded(self):
        """Test executing function from unloaded plugin."""
        result = self.plugin_manager.execute_plugin_function("nonexistent", "function")
        self.assertIsNone(result)
    
    def test_execute_plugin_function_not_found(self):
        """Test executing non-existent function."""
        plugin_content = '''
def existing_function():
    return "exists"
'''
        plugin_file = Path(self.temp_dir) / "test_plugin.py"
        plugin_file.write_text(plugin_content)
        
        self.plugin_manager.load_plugin("test_plugin")
        result = self.plugin_manager.execute_plugin_function("test_plugin", "nonexistent_function")
        self.assertIsNone(result)

class TestTaskScheduler(unittest.TestCase):
    """Test cases for the TaskScheduler class."""
    
    def setUp(self):
        """Set up test environment."""
        self.scheduler = TaskScheduler()
    
    def test_schedule_task_success(self):
        """Test successful task scheduling."""
        def test_task():
            return "task completed"
        
        success = self.scheduler.schedule_task("test_task", test_task, 5)
        self.assertTrue(success)
        self.assertIn("test_task", self.scheduler.scheduled_tasks)
    
    def test_run_once_success(self):
        """Test running a task once."""
        def test_task():
            return "task completed"
        
        success = self.scheduler.run_once("test_task", test_task)
        self.assertTrue(success)
        
        # Check history
        history = self.scheduler.list_task_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['task_name'], "test_task")
        self.assertTrue(history[0]['success'])
    
    def test_run_once_failure(self):
        """Test running a task that fails."""
        def failing_task():
            raise Exception("Task failed")
        
        success = self.scheduler.run_once("failing_task", failing_task)
        self.assertFalse(success)
        
        # Check history
        history = self.scheduler.list_task_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['task_name'], "failing_task")
        self.assertFalse(history[0]['success'])
    
    def test_cancel_task(self):
        """Test task cancellation."""
        def test_task():
            return "task"
        
        # Schedule and then cancel task
        self.scheduler.schedule_task("test_task", test_task, 5)
        self.assertIn("test_task", self.scheduler.scheduled_tasks)
        
        success = self.scheduler.cancel_task("test_task")
        self.assertTrue(success)
        self.assertNotIn("test_task", self.scheduler.scheduled_tasks)
    
    def test_cancel_nonexistent_task(self):
        """Test cancelling non-existent task."""
        success = self.scheduler.cancel_task("nonexistent_task")
        self.assertFalse(success)
    
    def test_list_scheduled_tasks(self):
        """Test listing scheduled tasks."""
        def task1():
            return "task1"
        
        def task2():
            return "task2"
        
        self.scheduler.schedule_task("task1", task1, 10)
        self.scheduler.schedule_task("task2", task2, 20)
        
        tasks = self.scheduler.list_scheduled_tasks()
        self.assertEqual(len(tasks), 2)
        
        task_names = [task['function'].__name__ for task in tasks]
        self.assertIn("task1", task_names)
        self.assertIn("task2", task_names)

class TestSandboxMode(unittest.TestCase):
    """Test cases for the SandboxMode class."""
    
    def setUp(self):
        """Set up test environment."""
        self.sandbox = SandboxMode()
    
    def test_sandbox_enabled_by_default(self):
        """Test that sandbox is enabled by default."""
        self.assertTrue(self.sandbox.is_sandbox_enabled())
    
    def test_enable_disable_sandbox(self):
        """Test enabling and disabling sandbox mode."""
        # Disable sandbox
        self.sandbox.disable_sandbox()
        self.assertFalse(self.sandbox.is_sandbox_enabled())
        
        # Enable sandbox
        self.sandbox.enable_sandbox()
        self.assertTrue(self.sandbox.is_sandbox_enabled())
    
    def test_is_lab_network(self):
        """Test lab network detection."""
        # Test valid lab networks
        self.assertTrue(self.sandbox.is_lab_network("192.168.1.100"))
        self.assertTrue(self.sandbox.is_lab_network("10.0.0.1"))
        self.assertTrue(self.sandbox.is_lab_network("172.16.0.1"))
        
        # Test non-lab networks
        self.assertFalse(self.sandbox.is_lab_network("8.8.8.8"))
        self.assertFalse(self.sandbox.is_lab_network("1.1.1.1"))
    
    def test_check_operation_safety_sandbox_disabled(self):
        """Test operation safety when sandbox is disabled."""
        self.sandbox.disable_sandbox()
        
        # All operations should be allowed when sandbox is disabled
        self.assertTrue(self.sandbox.check_operation_safety("ddos_simulator", "8.8.8.8"))
        self.assertTrue(self.sandbox.check_operation_safety("arp_spoofing", "1.1.1.1"))
    
    def test_check_operation_safety_sandbox_enabled(self):
        """Test operation safety when sandbox is enabled."""
        self.sandbox.enable_sandbox()
        
        # Destructive operations should be blocked on non-lab networks
        self.assertFalse(self.sandbox.check_operation_safety("ddos_simulator", "8.8.8.8"))
        self.assertFalse(self.sandbox.check_operation_safety("arp_spoofing", "1.1.1.1"))
        
        # Destructive operations should be allowed on lab networks
        self.assertTrue(self.sandbox.check_operation_safety("ddos_simulator", "192.168.1.100"))
        self.assertTrue(self.sandbox.check_operation_safety("arp_spoofing", "10.0.0.1"))
        
        # Non-destructive operations should be allowed
        self.assertTrue(self.sandbox.check_operation_safety("network_scanning", "8.8.8.8"))
        self.assertTrue(self.sandbox.check_operation_safety("web_testing", "1.1.1.1"))
    
    def test_add_remove_lab_network(self):
        """Test adding and removing lab networks."""
        # Add new lab network
        self.sandbox.add_lab_network("203.0.113.0/24")
        self.assertTrue(self.sandbox.is_lab_network("203.0.113.100"))
        
        # Remove lab network
        self.sandbox.remove_lab_network("203.0.113.0/24")
        self.assertFalse(self.sandbox.is_lab_network("203.0.113.100"))
    
    def test_add_invalid_network(self):
        """Test adding invalid network format."""
        # This should not raise an exception but log an error
        self.sandbox.add_lab_network("invalid_network")
        self.assertFalse(self.sandbox.is_lab_network("invalid_network"))
    
    def test_get_safety_info(self):
        """Test getting safety configuration information."""
        info = self.sandbox.get_safety_info()
        
        self.assertIn('sandbox_enabled', info)
        self.assertIn('lab_networks', info)
        self.assertIn('destructive_operations', info)
        self.assertIn('safety_checks', info)
        
        self.assertTrue(info['sandbox_enabled'])
        self.assertIsInstance(info['lab_networks'], list)
        self.assertIsInstance(info['destructive_operations'], dict)
        self.assertIsInstance(info['safety_checks'], dict)

class TestIntegration(unittest.TestCase):
    """Integration tests for the plugin system."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.plugin_manager = PluginManager()
        self.plugin_manager.plugins_dir = Path(self.temp_dir)
        self.scheduler = TaskScheduler()
        self.sandbox = SandboxMode()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_plugin_with_scheduler(self):
        """Test integrating plugins with the scheduler."""
        # Create a plugin with a function
        plugin_content = '''
def scheduled_task():
    return "Plugin task executed"
'''
        plugin_file = Path(self.temp_dir) / "scheduler_plugin.py"
        plugin_file.write_text(plugin_content)
        
        # Load plugin
        self.plugin_manager.load_plugin("scheduler_plugin")
        
        # Schedule plugin function
        success = self.scheduler.schedule_task(
            "plugin_task", 
            lambda: self.plugin_manager.execute_plugin_function("scheduler_plugin", "scheduled_task"),
            5
        )
        
        self.assertTrue(success)
        self.assertIn("plugin_task", self.scheduler.scheduled_tasks)
    
    def test_plugin_with_sandbox(self):
        """Test plugin execution with sandbox restrictions."""
        # Create a plugin that requires sandbox
        plugin_content = '''
__requires_sandbox__ = True

def destructive_operation():
    return "Destructive operation executed"
'''
        plugin_file = Path(self.temp_dir) / "destructive_plugin.py"
        plugin_file.write_text(plugin_content)
        
        # Load plugin
        self.plugin_manager.load_plugin("destructive_plugin")
        
        # Test with sandbox enabled (should work on lab network)
        self.sandbox.enable_sandbox()
        result = self.plugin_manager.execute_plugin_function("destructive_plugin", "destructive_operation")
        self.assertEqual(result, "Destructive operation executed")
        
        # Test with sandbox disabled (should also work)
        self.sandbox.disable_sandbox()
        result = self.plugin_manager.execute_plugin_function("destructive_plugin", "destructive_operation")
        self.assertEqual(result, "Destructive operation executed")

if __name__ == '__main__':
    unittest.main()
