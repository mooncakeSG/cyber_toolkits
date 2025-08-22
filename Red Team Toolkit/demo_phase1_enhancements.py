#!/usr/bin/env python3
"""
Enhanced Red Team Toolkit v2.1 - Phase 1 Core Enhancements Demo
This script demonstrates the new interactive CLI, configuration management, and logging features.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_enhanced_cli():
    """Demonstrate enhanced CLI features."""
    print("=" * 60)
    print("ENHANCED CLI FEATURES DEMO")
    print("=" * 60)
    
    from red_team_toolkit import cli_manager, config, RICH_AVAILABLE
    
    print("✓ CLI Manager initialized")
    print(f"✓ Rich library available: {RICH_AVAILABLE}")
    print(f"✓ Enhanced CLI enabled: {cli_manager.enable_rich}")
    print(f"✓ Show descriptions: {cli_manager.show_descriptions}")
    print(f"✓ Keyboard shortcuts: {cli_manager.enable_shortcuts}")
    print(f"✓ Confirm exit: {cli_manager.confirm_exit}")
    
    # Demo banner
    print("\nBanner Display:")
    cli_manager.print_banner()
    
    # Demo menu
    print("\nEnhanced Menu Display:")
    tools = [
        (1, "Port Scanner", "Multi-threaded port discovery"),
        (2, "Hash Generator", "Generate various hash types"),
        (3, "Configuration", "Settings management")
    ]
    cli_manager.print_menu(tools)
    
    # Demo help
    print("\nHelp System:")
    cli_manager.show_help()

def demo_configuration_management():
    """Demonstrate enhanced configuration management."""
    print("\n" + "=" * 60)
    print("CONFIGURATION MANAGEMENT DEMO")
    print("=" * 60)
    
    from red_team_toolkit import config, cli_manager, RICH_AVAILABLE
    
    print("✓ Configuration system loaded")
    print(f"Config file: {config.config_file}")
    
    # Show current configuration
    print("\nCurrent Configuration:")
    if cli_manager.enable_rich and RICH_AVAILABLE:
        from red_team_toolkit import view_configuration
        view_configuration()
    else:
        for section in config.config.sections():
            print(f"\n[{section}]")
            for option, value in config.config.items(section):
                print(f"  {option} = {value}")
    
    # Test configuration access
    max_threads = config.getint('DEFAULT', 'max_threads')
    save_reports = config.getboolean('DEFAULT', 'save_reports')
    enable_rich = config.getboolean('DEFAULT', 'enable_rich_cli')
    
    print(f"\n✓ Max threads: {max_threads}")
    print(f"✓ Save reports: {save_reports}")
    print(f"✓ Enable Rich CLI: {enable_rich}")
    
    # Test new configuration options
    print(f"✓ Show banner: {config.getboolean('CLI', 'show_banner')}")
    print(f"✓ Auto clear screen: {config.getboolean('CLI', 'auto_clear_screen')}")
    print(f"✓ Log level: {config.get('LOGGING', 'log_level')}")

def demo_enhanced_logging():
    """Demonstrate enhanced logging system."""
    print("\n" + "=" * 60)
    print("ENHANCED LOGGING DEMO")
    print("=" * 60)
    
    from red_team_toolkit import logger, config
    
    print("✓ Enhanced logging system initialized")
    print(f"Log file: {config.get('LOGGING', 'log_file')}")
    print(f"Log level: {config.get('LOGGING', 'log_level')}")
    print(f"Log format: {config.get('LOGGING', 'log_format')}")
    
    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    print("✓ Log messages written to file and console")
    
    # Check if log file exists
    log_file = Path(config.get('LOGGING', 'log_file'))
    if log_file.exists():
        print(f"✓ Log file created: {log_file}")
        print(f"✓ Log file size: {log_file.stat().st_size} bytes")
    else:
        print("⚠️  Log file not found")

def demo_enhanced_progress_bars():
    """Demonstrate enhanced progress bar system."""
    print("\n" + "=" * 60)
    print("ENHANCED PROGRESS BARS DEMO")
    print("=" * 60)
    
    from red_team_toolkit import ProgressBar, config, RICH_AVAILABLE, TQDM_AVAILABLE
    import time
    
    print("✓ Progress bar system initialized")
    print(f"✓ Rich available: {RICH_AVAILABLE}")
    print(f"✓ TQDM available: {TQDM_AVAILABLE}")
    print(f"✓ Progress bars enabled: {config.getboolean('DEFAULT', 'enable_progress_bars')}")
    
    # Test progress bar
    print("\nTesting progress bar (10 items):")
    progress = ProgressBar(10, "Demo Progress")
    
    for i in range(10):
        time.sleep(0.2)  # Simulate work
        progress.update()
    
    progress.finish()

def demo_enhanced_input_handling():
    """Demonstrate enhanced input handling."""
    print("\n" + "=" * 60)
    print("ENHANCED INPUT HANDLING DEMO")
    print("=" * 60)
    
    from red_team_toolkit import safe_input, safe_confirm, cli_manager, RICH_AVAILABLE
    
    print("✓ Enhanced input functions available")
    print(f"✓ Rich input enabled: {cli_manager.enable_rich and RICH_AVAILABLE}")
    
    # Test safe input
    print("\nTesting safe input (type 'test' or press Ctrl+C):")
    try:
        result = safe_input("Enter some text")
        if result:
            print(f"✓ Input received: {result}")
        else:
            print("✓ Input cancelled")
    except KeyboardInterrupt:
        print("✓ Keyboard interrupt handled gracefully")
    
    # Test confirmation
    print("\nTesting confirmation (type 'n' to skip):")
    try:
        confirmed = safe_confirm("Do you want to continue?")
        print(f"✓ Confirmation result: {confirmed}")
    except KeyboardInterrupt:
        print("✓ Keyboard interrupt handled gracefully")

def demo_keyboard_shortcuts():
    """Demonstrate keyboard shortcuts."""
    print("\n" + "=" * 60)
    print("KEYBOARD SHORTCUTS DEMO")
    print("=" * 60)
    
    from red_team_toolkit import cli_manager
    
    print("✓ Keyboard shortcuts system available")
    print(f"✓ Shortcuts enabled: {cli_manager.enable_shortcuts}")
    
    print("\nAvailable shortcuts:")
    print("  • 0, q, quit, exit - Exit the toolkit")
    print("  • h, help - Show help information")
    print("  • Ctrl+C - Abort current operation")
    
    print("\nShortcut handling:")
    print("  • All shortcuts are handled gracefully")
    print("  • No crashes on unexpected input")
    print("  • Clear feedback for user actions")

def demo_error_handling():
    """Demonstrate enhanced error handling."""
    print("\n" + "=" * 60)
    print("ENHANCED ERROR HANDLING DEMO")
    print("=" * 60)
    
    from red_team_toolkit import cli_manager, logger, RICH_AVAILABLE
    
    print("✓ Enhanced error handling system")
    
    # Test error display
    test_error = "This is a test error message"
    
    if cli_manager.enable_rich and RICH_AVAILABLE:
        cli_manager.console.print(f"[red]❌ Error: {test_error}[/red]")
        cli_manager.console.print("[yellow]⚠️  Warning: This is a test warning[/yellow]")
        cli_manager.console.print("[green]✓ Success: This is a test success message[/green]")
    else:
        from red_team_toolkit import colored, Colors
        print(colored(f"❌ Error: {test_error}", Colors.FAIL))
        print(colored("⚠️  Warning: This is a test warning", Colors.WARNING))
        print(colored("✓ Success: This is a test success message", Colors.OKGREEN))
    
    # Test logging
    logger.error("Test error logged")
    logger.warning("Test warning logged")
    logger.info("Test info logged")
    
    print("✓ Error messages logged to file")

def main():
    """Run all Phase 1 enhancement demonstrations."""
    print("Enhanced Red Team Toolkit v2.1 - Phase 1 Core Enhancements")
    print("=" * 60)
    print("This demo showcases the new interactive CLI, configuration management,")
    print("and logging features added in Phase 1.")
    print("=" * 60)
    
    demos = [
        ("Enhanced CLI Features", demo_enhanced_cli),
        ("Configuration Management", demo_configuration_management),
        ("Enhanced Logging", demo_enhanced_logging),
        ("Enhanced Progress Bars", demo_enhanced_progress_bars),
        ("Enhanced Input Handling", demo_enhanced_input_handling),
        ("Keyboard Shortcuts", demo_keyboard_shortcuts),
        ("Enhanced Error Handling", demo_error_handling)
    ]
    
    for demo_name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ Error in {demo_name}: {e}")
    
    print("\n" + "=" * 60)
    print("PHASE 1 DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("Phase 1 enhancements include:")
    print("✓ Interactive CLI with Rich support")
    print("✓ Enhanced configuration management")
    print("✓ Comprehensive logging system")
    print("✓ Advanced progress bars (Rich/tqdm)")
    print("✓ Keyboard shortcuts and navigation")
    print("✓ Enhanced error handling")
    print("✓ Better user experience")
    
    print("\nTo run the full enhanced toolkit:")
    print("python red_team_toolkit.py")
    
    print("\nTo install new dependencies:")
    print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
