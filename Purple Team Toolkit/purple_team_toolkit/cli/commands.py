"""
CLI Commands for Purple Team Toolkit
"""

import click
import yaml
import json
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional

from ..purple_logic import PurpleTeamEngine
from ..config import Config

console = Console()

@click.group()
@click.version_option(version="1.0.0")
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.pass_context
def main(ctx, verbose: bool, config: Optional[str]):
    """Purple Team Toolkit - Attack-Defense Correlation Framework"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    
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
@click.pass_context
def run_scenario(ctx, scenario: str, sandbox: bool, output: Optional[str]):
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
            results = engine.execute_scenario(scenario_config)
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
            display_scenario_summary(results)
            
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
@click.pass_context
def report(ctx, format: str, output: str, scenario_results: Optional[str]):
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
            report_content = engine.generate_report(results, format)
            
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
    table.add_column("File", style="dim")
    
    scenario_files = list(scenarios_dir.glob("*.yaml")) + list(scenarios_dir.glob("*.yml"))
    
    for scenario_file in scenario_files:
        try:
            with open(scenario_file, 'r') as f:
                scenario_data = yaml.safe_load(f)
            
            name = scenario_data.get('name', scenario_file.stem)
            description = scenario_data.get('description', 'No description available')
            
            table.add_row(name, description, str(scenario_file))
            
        except Exception as e:
            table.add_row(scenario_file.stem, f"Error loading: {e}", str(scenario_file))
    
    console.print(table)

def display_scenario_summary(results: dict):
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
    
    console.print(table)

if __name__ == '__main__':
    main()
