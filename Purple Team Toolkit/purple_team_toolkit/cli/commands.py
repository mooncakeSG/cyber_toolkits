"""
CLI Commands for Purple Team Toolkit
"""

import click
import yaml
import json
import os
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree
from rich.live import Live
from rich.layout import Layout
from typing import Optional, List

from ..purple_logic import PurpleTeamEngine
from ..red_team import RedTeamModule
from ..blue_team import BlueTeamModule
from ..config import Config

console = Console()

@click.group()
@click.version_option(version="1.0.0")
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--log-level', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']), 
              default='INFO', help='Logging level')
@click.pass_context
def main(ctx, verbose: bool, config: Optional[str], log_level: str):
    """Purple Team Toolkit - Attack-Defense Correlation Framework"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['log_level'] = log_level
    
    # Load configuration
    if config:
        ctx.obj['config'] = Config.from_file(config)
    else:
        ctx.obj['config'] = Config.default()

@main.command()
@click.option('--scenario', '-s', type=click.Path(exists=True), required=True, 
              help='Path to scenario configuration file')
@click.option('--sandbox', is_flag=True, help='Enable sandbox mode for safe testing')
@click.option('--output', '-o', type=click.Path(), help='Output directory for results')
@click.option('--timeout', type=int, default=3600, help='Scenario timeout in seconds')
@click.option('--parallel', is_flag=True, help='Execute attacks in parallel')
@click.pass_context
def run_scenario(ctx, scenario: str, sandbox: bool, output: Optional[str], 
                timeout: int, parallel: bool):
    """Execute a full attack and defense scenario"""
    
    console.print(Panel.fit(
        "[bold blue]Purple Team Toolkit - Scenario Execution[/bold blue]",
        border_style="blue"
    ))
    
    # Load scenario configuration
    try:
        with open(scenario, 'r') as f:
            scenario_config = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]Error loading scenario: {e}[/red]")
        return
    
    # Initialize Purple Team Engine
    config = ctx.obj['config']
    if sandbox:
        config.sandbox_mode = True
    
    engine = PurpleTeamEngine(config)
    
    # Execute scenario
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Executing scenario...", total=None)
        
        try:
            start_time = time.time()
            results = engine.execute_scenario(scenario_config, timeout=timeout, parallel=parallel)
            execution_time = time.time() - start_time
            
            progress.update(task, description="Scenario completed successfully!")
            
            # Save results
            if output:
                output_path = Path(output)
                output_path.mkdir(parents=True, exist_ok=True)
                
                results_file = output_path / "scenario_results.json"
                with open(results_file, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                
                console.print(f"[green]Results saved to: {results_file}[/green]")
            
            # Display summary
            display_scenario_summary(results, execution_time)
            
        except Exception as e:
            progress.update(task, description="Scenario failed!")
            console.print(f"[red]Error executing scenario: {e}[/red]")
            if ctx.obj['verbose']:
                raise

@main.command()
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'html', 'pdf']), 
              default='html', help='Output format')
@click.option('--output', '-o', type=click.Path(), required=True, help='Output file path')
@click.option('--scenario-results', type=click.Path(exists=True), 
              help='Path to scenario results file')
@click.option('--template', type=click.Path(exists=True), help='Custom report template')
@click.pass_context
def report(ctx, format: str, output: str, scenario_results: Optional[str], template: Optional[str]):
    """Generate scenario detection and coverage report"""
    
    console.print(Panel.fit(
        "[bold green]Purple Team Toolkit - Report Generation[/bold green]",
        border_style="green"
    ))
    
    # Load results
    if scenario_results:
        with open(scenario_results, 'r') as f:
            results = json.load(f)
    else:
        # Look for latest results
        results_dir = Path("reports")
        if results_dir.exists():
            result_files = list(results_dir.glob("scenario_results.json"))
            if result_files:
                latest = max(result_files, key=lambda x: x.stat().st_mtime)
                with open(latest, 'r') as f:
                    results = json.load(f)
            else:
                console.print("[red]No scenario results found. Run a scenario first.[/red]")
                return
        else:
            console.print("[red]No scenario results found. Run a scenario first.[/red]")
            return
    
    # Generate report
    config = ctx.obj['config']
    engine = PurpleTeamEngine(config)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Generating report...", total=None)
        
        try:
            report_content = engine.generate_report(results, format, template)
            
            # Save report
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if format == 'json':
                with open(output_path, 'w') as f:
                    json.dump(report_content, f, indent=2, default=str)
            else:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
            
            progress.update(task, description="Report generated successfully!")
            console.print(f"[green]Report saved to: {output_path}[/green]")
            
        except Exception as e:
            progress.update(task, description="Report generation failed!")
            console.print(f"[red]Error generating report: {e}[/red]")
            if ctx.obj['verbose']:
                raise

@main.command()
@click.pass_context
def list_scenarios(ctx):
    """List available predefined attack-defense scenarios"""
    
    console.print(Panel.fit(
        "[bold yellow]Purple Team Toolkit - Available Scenarios[/bold yellow]",
        border_style="yellow"
    ))
    
    scenarios_dir = Path("configs/scenarios")
    if not scenarios_dir.exists():
        console.print("[red]Scenarios directory not found.[/red]")
        return
    
    table = Table(title="Available Scenarios")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Difficulty", style="yellow")
    table.add_column("File", style="dim")
    
    scenario_files = list(scenarios_dir.glob("*.yaml")) + list(scenarios_dir.glob("*.yml"))
    
    for scenario_file in scenario_files:
        try:
            with open(scenario_file, 'r') as f:
                scenario_data = yaml.safe_load(f)
            
            name = scenario_data.get('name', scenario_file.stem)
            description = scenario_data.get('description', 'No description available')
            difficulty = scenario_data.get('difficulty', 'Medium')
            
            table.add_row(name, description, difficulty, str(scenario_file))
            
        except Exception as e:
            table.add_row(scenario_file.stem, f"Error loading: {e}", "Unknown", str(scenario_file))
    
    console.print(table)

@main.group()
def red_team():
    """Red Team operations"""
    pass

@red_team.command()
@click.option('--target', '-t', required=True, help='Target IP/domain')
@click.option('--scan-type', type=click.Choice(['basic', 'full', 'stealth']), 
              default='basic', help='Scan type')
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
@click.pass_context
def recon(ctx, target: str, scan_type: str, output: Optional[str]):
    """Perform reconnaissance on target"""
    
    console.print(Panel.fit(
        f"[bold red]Red Team - Reconnaissance on {target}[/bold red]",
        border_style="red"
    ))
    
    config = ctx.obj['config']
    red_team = RedTeamModule(config)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Performing reconnaissance...", total=None)
        
        try:
            results = red_team.reconnaissance.perform_reconnaissance(target, scan_type)
            
            progress.update(task, description="Reconnaissance completed!")
            
            # Display results
            display_recon_results(results)
            
            # Save results
            if output:
                with open(output, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                console.print(f"[green]Results saved to: {output}[/green]")
                
        except Exception as e:
            progress.update(task, description="Reconnaissance failed!")
            console.print(f"[red]Error: {e}[/red]")

@red_team.command()
@click.option('--target', '-t', required=True, help='Target URL/IP')
@click.option('--exploit-type', type=click.Choice(['web', 'network', 'social']), 
              default='web', help='Exploitation type')
@click.option('--payload', '-p', help='Custom payload')
@click.pass_context
def exploit(ctx, target: str, exploit_type: str, payload: Optional[str]):
    """Execute exploitation techniques"""
    
    console.print(Panel.fit(
        f"[bold red]Red Team - Exploitation on {target}[/bold red]",
        border_style="red"
    ))
    
    config = ctx.obj['config']
    red_team = RedTeamModule(config)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Executing exploitation...", total=None)
        
        try:
            results = red_team.exploitation.execute_exploitation(target, exploit_type, payload)
            
            progress.update(task, description="Exploitation completed!")
            display_exploit_results(results)
                
        except Exception as e:
            progress.update(task, description="Exploitation failed!")
            console.print(f"[red]Error: {e}[/red]")

@main.group()
def blue_team():
    """Blue Team operations"""
    pass

@blue_team.command()
@click.option('--source', '-s', multiple=True, help='Log sources to monitor')
@click.option('--duration', '-d', type=int, default=300, help='Monitoring duration in seconds')
@click.option('--output', '-o', type=click.Path(), help='Output file for alerts')
@click.pass_context
def monitor(ctx, source: List[str], duration: int, output: Optional[str]):
    """Start security monitoring"""
    
    console.print(Panel.fit(
        "[bold blue]Blue Team - Security Monitoring[/bold blue]",
        border_style="blue"
    ))
    
    config = ctx.obj['config']
    blue_team = BlueTeamModule(config)
    
    sources = source if source else ['system_logs', 'network_logs', 'security_logs']
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task(f"Monitoring for {duration}s...", total=duration)
        
        try:
            alerts = blue_team.log_collector.monitor_logs(sources, duration)
            
            progress.update(task, description="Monitoring completed!")
            
            # Display alerts
            display_alerts(alerts)
            
            # Save alerts
            if output:
                with open(output, 'w') as f:
                    json.dump(alerts, f, indent=2, default=str)
                console.print(f"[green]Alerts saved to: {output}[/green]")
                
        except Exception as e:
            progress.update(task, description="Monitoring failed!")
            console.print(f"[red]Error: {e}[/red]")

@blue_team.command()
@click.option('--query', '-q', required=True, help='Threat hunting query')
@click.option('--timeframe', '-t', default='24h', help='Timeframe for hunting')
@click.pass_context
def hunt(ctx, query: str, timeframe: str):
    """Perform threat hunting"""
    
    console.print(Panel.fit(
        "[bold blue]Blue Team - Threat Hunting[/bold blue]",
        border_style="blue"
    ))
    
    config = ctx.obj['config']
    blue_team = BlueTeamModule(config)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Performing threat hunt...", total=None)
        
        try:
            results = blue_team.detection_engine.threat_hunt(query, timeframe)
            
            progress.update(task, description="Threat hunt completed!")
            display_hunt_results(results)
                
        except Exception as e:
            progress.update(task, description="Threat hunt failed!")
            console.print(f"[red]Error: {e}[/red]")

@main.command()
@click.option('--target', '-t', required=True, help='Target to analyze')
@click.option('--techniques', multiple=True, help='MITRE ATT&CK techniques to test')
@click.option('--output', '-o', type=click.Path(), help='Output file for analysis')
@click.pass_context
def analyze(ctx, target: str, techniques: List[str], output: Optional[str]):
    """Analyze detection coverage for specific techniques"""
    
    console.print(Panel.fit(
        "[bold purple]Purple Team - Coverage Analysis[/bold purple]",
        border_style="purple"
    ))
    
    config = ctx.obj['config']
    engine = PurpleTeamEngine(config)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Analyzing coverage...", total=None)
        
        try:
            analysis = engine.analyze_coverage(target, techniques)
            
            progress.update(task, description="Analysis completed!")
            display_coverage_analysis(analysis)
            
            # Save analysis
            if output:
                with open(output, 'w') as f:
                    json.dump(analysis, f, indent=2, default=str)
                console.print(f"[green]Analysis saved to: {output}[/green]")
                
        except Exception as e:
            progress.update(task, description="Analysis failed!")
            console.print(f"[red]Error: {e}[/red]")

@main.command()
@click.pass_context
def status(ctx):
    """Show toolkit status and health"""
    
    console.print(Panel.fit(
        "[bold cyan]Purple Team Toolkit - Status[/bold cyan]",
        border_style="cyan"
    ))
    
    config = ctx.obj['config']
    
    # Check toolkit components
    table = Table(title="Toolkit Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Details", style="dim")
    
    # Red Team status
    try:
        red_team = RedTeamModule(config)
        table.add_row("Red Team", "✅ Active", "Ready for operations")
    except Exception as e:
        table.add_row("Red Team", "❌ Error", str(e))
    
    # Blue Team status
    try:
        blue_team = BlueTeamModule(config)
        table.add_row("Blue Team", "✅ Active", "Ready for operations")
    except Exception as e:
        table.add_row("Blue Team", "❌ Error", str(e))
    
    # Purple Logic status
    try:
        engine = PurpleTeamEngine(config)
        table.add_row("Purple Logic", "✅ Active", "Ready for correlation")
    except Exception as e:
        table.add_row("Purple Logic", "❌ Error", str(e))
    
    # Configuration status
    if config.sandbox_mode:
        table.add_row("Sandbox Mode", "🟡 Enabled", "Safe testing mode")
    else:
        table.add_row("Sandbox Mode", "🔴 Disabled", "Production mode")
    
    console.print(table)

def display_scenario_summary(results: dict, execution_time: float):
    """Display a summary of scenario execution results"""
    
    table = Table(title="Scenario Execution Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    
    # Attack summary
    attacks = results.get('red_team', {}).get('attacks', [])
    table.add_row("Attacks Executed", str(len(attacks)))
    
    # Detection summary
    detections = results.get('blue_team', {}).get('detections', [])
    table.add_row("Detections Triggered", str(len(detections)))
    
    # Coverage analysis
    coverage = results.get('purple_logic', {}).get('coverage', {})
    detected = coverage.get('detected', 0)
    total = coverage.get('total', 0)
    coverage_percent = (detected / total * 100) if total > 0 else 0
    
    table.add_row("Detection Coverage", f"{detected}/{total} ({coverage_percent:.1f}%)")
    
    # Score
    score = results.get('purple_logic', {}).get('score', 0)
    table.add_row("Overall Score", f"{score:.1f}/100")
    
    # Execution time
    table.add_row("Execution Time", f"{execution_time:.2f} seconds")
    
    console.print(table)

def display_recon_results(results: dict):
    """Display reconnaissance results"""
    
    table = Table(title="Reconnaissance Results")
    table.add_column("Technique", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Details", style="dim")
    
    for result in results.get('results', []):
        status = "✅ Success" if result.get('success') else "❌ Failed"
        details = result.get('description', 'No details')
        table.add_row(result.get('technique', 'Unknown'), status, details)
    
    console.print(table)

def display_exploit_results(results: dict):
    """Display exploitation results"""
    
    table = Table(title="Exploitation Results")
    table.add_column("Technique", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Details", style="dim")
    
    for result in results.get('results', []):
        status = "✅ Success" if result.get('success') else "❌ Failed"
        details = result.get('description', 'No details')
        table.add_row(result.get('technique', 'Unknown'), status, details)
    
    console.print(table)

def display_alerts(alerts: List[dict]):
    """Display security alerts"""
    
    if not alerts:
        console.print("[yellow]No alerts detected during monitoring period.[/yellow]")
        return
    
    table = Table(title="Security Alerts")
    table.add_column("Time", style="cyan")
    table.add_column("Severity", style="white")
    table.add_column("Source", style="dim")
    table.add_column("Description", style="white")
    
    for alert in alerts:
        severity_color = {
            'critical': 'red',
            'high': 'yellow',
            'medium': 'blue',
            'low': 'green'
        }.get(alert.get('severity', 'medium'), 'white')
        
        table.add_row(
            alert.get('timestamp', 'Unknown'),
            f"[{severity_color}]{alert.get('severity', 'Unknown')}[/{severity_color}]",
            alert.get('source', 'Unknown'),
            alert.get('description', 'No description')
        )
    
    console.print(table)

def display_hunt_results(results: List[dict]):
    """Display threat hunting results"""
    
    if not results:
        console.print("[yellow]No threats found during hunt.[/yellow]")
        return
    
    table = Table(title="Threat Hunting Results")
    table.add_column("Indicator", style="cyan")
    table.add_column("Type", style="white")
    table.add_column("Confidence", style="dim")
    table.add_column("Description", style="white")
    
    for result in results:
        table.add_row(
            result.get('indicator', 'Unknown'),
            result.get('type', 'Unknown'),
            f"{result.get('confidence', 0)}%",
            result.get('description', 'No description')
        )
    
    console.print(table)

def display_coverage_analysis(analysis: dict):
    """Display coverage analysis results"""
    
    table = Table(title="Detection Coverage Analysis")
    table.add_column("Technique", style="cyan")
    table.add_column("Coverage", style="white")
    table.add_column("Status", style="dim")
    
    for technique, coverage in analysis.get('techniques', {}).items():
        coverage_percent = coverage.get('coverage', 0)
        status = "✅ Detected" if coverage_percent > 0 else "❌ Not Detected"
        
        table.add_row(
            technique,
            f"{coverage_percent:.1f}%",
            status
        )
    
    overall_coverage = analysis.get('overall_coverage', 0)
    console.print(table)
    console.print(f"[bold]Overall Coverage: {overall_coverage:.1f}%[/bold]")

if __name__ == '__main__':
    main()
