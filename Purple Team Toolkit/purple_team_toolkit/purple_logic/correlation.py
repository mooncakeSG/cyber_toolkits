"""
Purple Team Correlation Engine

Correlates Red Team attack activities with Blue Team detections
and provides coverage analysis and reporting.
"""

import json
import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
import pandas as pd
from jinja2 import Template

from ..red_team import ReconnaissanceModule, ExploitationModule, PostExploitationModule, PayloadManager
from ..blue_team import LogCollector, DetectionEngine, AlertManager
from ..blue_team.normalization import EventNormalizer, NormalizedEvent
from ..config import Config

@dataclass
class CorrelationResult:
    """Result of attack-detection correlation"""
    attack_technique: str
    expected_detection: str
    actual_detection: Optional[str]
    detected: bool
    detection_time: Optional[float] = None
    false_positive: bool = False
    false_negative: bool = False
    mitre_technique: Optional[str] = None
    confidence: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CoverageAnalysis:
    """Analysis of detection coverage"""
    total_attacks: int
    detected_attacks: int
    coverage_percentage: float
    false_positives: int
    false_negatives: int
    accuracy: float
    mitre_coverage: Dict[str, Dict[str, Any]]
    recommendations: List[str]
    score: float

class PurpleTeamEngine:
    """Main Purple Team correlation engine"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize Red Team modules
        self.recon_module = ReconnaissanceModule(config.red_team_modules)
        self.exploitation_module = ExploitationModule(config.red_team_modules)
        self.post_exploitation_module = PostExploitationModule(config.red_team_modules)
        self.payload_manager = PayloadManager(config.red_team_modules)
        
        # Initialize Blue Team modules
        self.log_collector = LogCollector(config.blue_team_modules)
        self.detection_engine = DetectionEngine(config.blue_team_modules)
        self.alert_manager = AlertManager(config.blue_team_modules)
        self.event_normalizer = EventNormalizer(config.blue_team_modules)
        
        # Correlation state
        self.attack_results: List[Dict[str, Any]] = []
        self.detection_results: List[Dict[str, Any]] = []
        self.correlation_results: List[CorrelationResult] = []
        
        # Setup logging
        config.setup_logging()
    
    def execute_scenario(self, scenario_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a complete Purple Team scenario"""
        self.logger.info("Starting Purple Team scenario execution")
        
        # Reset state
        self.attack_results = []
        self.detection_results = []
        self.correlation_results = []
        
        scenario_name = scenario_config.get('name', 'Unknown Scenario')
        self.logger.info(f"Executing scenario: {scenario_name}")
        
        # Execute Red Team activities
        red_team_results = self._execute_red_team_activities(scenario_config.get('red_team', []))
        
        # Execute Blue Team monitoring
        blue_team_results = self._execute_blue_team_monitoring(scenario_config.get('blue_team', []))
        
        # Correlate results
        correlation_results = self._correlate_attacks_and_detections(
            red_team_results, 
            blue_team_results,
            scenario_config.get('purple_logic', {}).get('correlation_rules', [])
        )
        
        # Analyze coverage
        coverage_analysis = self._analyze_coverage(correlation_results)
        
        # Generate comprehensive results
        results = {
            'scenario_name': scenario_name,
            'execution_time': datetime.now().isoformat(),
            'red_team': {
                'attacks': red_team_results,
                'total_attacks': len(red_team_results)
            },
            'blue_team': {
                'detections': blue_team_results,
                'total_detections': len(blue_team_results)
            },
            'purple_logic': {
                'correlations': [self._correlation_to_dict(corr) for corr in correlation_results],
                'coverage': self._coverage_to_dict(coverage_analysis),
                'score': coverage_analysis.score
            }
        }
        
        self.logger.info(f"Scenario completed. Coverage: {coverage_analysis.coverage_percentage:.1f}%")
        
        return results
    
    def _execute_red_team_activities(self, activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute Red Team attack activities"""
        results = []
        
        for activity in activities:
            try:
                module = activity.get('module')
                technique = activity.get('technique')
                target = activity.get('target')
                parameters = activity.get('parameters', {})
                
                self.logger.info(f"Executing Red Team activity: {module}.{technique} on {target}")
                
                if module == 'recon':
                    result = self._execute_recon_activity(technique, target, parameters)
                elif module == 'exploitation':
                    result = self._execute_exploitation_activity(technique, target, parameters)
                elif module == 'post_exploitation':
                    result = self._execute_post_exploitation_activity(technique, target, parameters)
                else:
                    self.logger.warning(f"Unknown Red Team module: {module}")
                    continue
                
                if result:
                    results.append(result)
                    
            except Exception as e:
                self.logger.error(f"Error executing Red Team activity: {e}")
                continue
        
        return results
    
    def _execute_recon_activity(self, technique: str, target: str, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute reconnaissance activity"""
        if technique == 'nmap_scan':
            scan_type = parameters.get('scan_type', 'basic')
            result = self.recon_module.nmap_scan(target, scan_type)
        elif technique == 'dns_enumeration':
            result = self.recon_module.dns_enumeration(target)
        elif technique == 'whois_lookup':
            result = self.recon_module.whois_lookup(target)
        else:
            self.logger.warning(f"Unknown reconnaissance technique: {technique}")
            return None
        
        return {
            'module': 'recon',
            'technique': technique,
            'target': target,
            'result': result,
            'timestamp': time.time()
        }
    
    def _execute_exploitation_activity(self, technique: str, target: str, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute exploitation activity"""
        if technique == 'web_fuzzing':
            wordlist = parameters.get('wordlist')
            result = self.exploitation_module.web_fuzzing(target, wordlist)
        elif technique == 'port_scan':
            ports = parameters.get('ports')
            result = self.exploitation_module.port_scan(target, ports)
        else:
            self.logger.warning(f"Unknown exploitation technique: {technique}")
            return None
        
        return {
            'module': 'exploitation',
            'technique': technique,
            'target': target,
            'result': result,
            'timestamp': time.time()
        }
    
    def _execute_post_exploitation_activity(self, technique: str, target: str, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute post-exploitation activity"""
        if technique == 'lateral_movement':
            result = self.post_exploitation_module.lateral_movement_simulation(target)
        elif technique == 'persistence':
            result = self.post_exploitation_module.persistence_simulation(target)
        else:
            self.logger.warning(f"Unknown post-exploitation technique: {technique}")
            return None
        
        return {
            'module': 'post_exploitation',
            'technique': technique,
            'target': target,
            'result': result,
            'timestamp': time.time()
        }
    
    def _execute_blue_team_monitoring(self, monitoring_config: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute Blue Team monitoring activities"""
        results = []
        
        # Handle different monitoring config formats
        if not monitoring_config:
            # Default sources if no config provided
            log_sources = ['system_logs', 'network_logs', 'application_logs', 'security_logs']
            for source in log_sources:
                try:
                    self.logger.info(f"Collecting logs from: {source}")
                    events = self.log_collector.collect_logs(source)
                    
                    # Normalize events
                    normalized_events = self.event_normalizer.normalize_events(events)
                    
                    # Apply detection rules
                    detected_events = self.detection_engine.detect_events(events)
                    
                    # Process alerts
                    alerts = self.alert_manager.process_alerts(detected_events)
                    
                    results.extend([
                        {
                            'source': source,
                            'event': event,
                            'normalized': normalized_event,
                            'detected': detected_event,
                            'alert': alert,
                            'timestamp': time.time()
                        }
                        for event, normalized_event, detected_event, alert in zip(
                            events, normalized_events, detected_events, alerts
                        )
                    ])
                except Exception as e:
                    self.logger.error(f"Error in Blue Team monitoring for {source}: {e}")
                    continue
        else:
            # Process structured monitoring config
            for monitoring_item in monitoring_config:
                try:
                    module = monitoring_item.get('module', 'unknown')
                    detection = monitoring_item.get('detection', 'unknown')
                    sources = monitoring_item.get('sources', [])
                    
                    self.logger.info(f"Collecting logs from: {monitoring_item}")
                    
                    # Collect from all sources for this monitoring item
                    for source in sources:
                        events = self.log_collector.collect_logs(source)
                        
                        # Normalize events
                        normalized_events = self.event_normalizer.normalize_events(events)
                        
                        # Apply detection rules
                        detected_events = self.detection_engine.detect_events(events)
                        
                        # Process alerts
                        alerts = self.alert_manager.process_alerts(detected_events)
                        
                        results.extend([
                            {
                                'source': source,
                                'module': module,
                                'detection': detection,
                                'event': event,
                                'normalized': normalized_event,
                                'detected': detected_event,
                                'alert': alert,
                                'timestamp': time.time()
                            }
                            for event, normalized_event, detected_event, alert in zip(
                                events, normalized_events, detected_events, alerts
                            )
                        ])
                
                except Exception as e:
                    self.logger.error(f"Error in Blue Team monitoring for {monitoring_item}: {e}")
                    continue
        
        return results
    
    def _correlate_attacks_and_detections(self, attacks: List[Dict[str, Any]], 
                                        detections: List[Dict[str, Any]], 
                                        correlation_rules: List[Dict[str, Any]]) -> List[CorrelationResult]:
        """Correlate Red Team attacks with Blue Team detections"""
        correlations = []
        
        for attack in attacks:
            attack_technique = attack['technique']
            attack_result = attack['result']
            
            # Find matching correlation rule
            matching_rule = None
            for rule in correlation_rules:
                if rule.get('attack') == attack_technique:
                    matching_rule = rule
                    break
            
            if not matching_rule:
                # Create default correlation
                correlation = CorrelationResult(
                    attack_technique=attack_technique,
                    expected_detection="unknown",
                    actual_detection=None,
                    detected=False,
                    mitre_technique=attack_result.mitre_technique,
                    confidence=0.0
                )
                correlations.append(correlation)
                continue
            
            expected_detection = matching_rule.get('expected_detection', 'unknown')
            
            # Look for matching detection
            actual_detection = None
            detection_time = None
            detected = False
            
            for detection in detections:
                if self._matches_detection(attack_technique, detection, expected_detection):
                    actual_detection = detection['event']['event_type']
                    detection_time = detection['timestamp']
                    detected = True
                    break
            
            # Calculate confidence
            confidence = self._calculate_correlation_confidence(attack, detections, expected_detection)
            
            correlation = CorrelationResult(
                attack_technique=attack_technique,
                expected_detection=expected_detection,
                actual_detection=actual_detection,
                detected=detected,
                detection_time=detection_time,
                mitre_technique=attack_result.mitre_technique,
                confidence=confidence,
                details={
                    'attack_data': attack_result.data,
                    'detection_data': [d['event'] for d in detections if d['detected']]
                }
            )
            
            correlations.append(correlation)
        
        return correlations
    
    def _matches_detection(self, attack_technique: str, detection: Dict[str, Any], expected_detection: str) -> bool:
        """Check if a detection matches an attack"""
        detection_event = detection['event']
        
        # Check if detection type matches expected
        if expected_detection in detection_event.get('event_type', ''):
            return True
        
        # Check MITRE technique match
        if detection_event.get('mitre_technique') and detection_event['mitre_technique'] == expected_detection:
            return True
        
        # Check description keywords
        description = detection_event.get('description', '').lower()
        attack_keywords = attack_technique.lower().replace('_', ' ')
        
        if attack_keywords in description:
            return True
        
        return False
    
    def _calculate_correlation_confidence(self, attack: Dict[str, Any], 
                                        detections: List[Dict[str, Any]], 
                                        expected_detection: str) -> float:
        """Calculate confidence level for correlation"""
        confidence = 0.0
        
        # Base confidence for having a detection rule
        if expected_detection != 'unknown':
            confidence += 0.3
        
        # Check for MITRE technique match
        attack_result = attack['result']
        if attack_result.mitre_technique:
            for detection in detections:
                if detection['event'].get('mitre_technique') == attack_result.mitre_technique:
                    confidence += 0.4
                    break
        
        # Check for temporal proximity
        attack_time = attack['timestamp']
        for detection in detections:
            detection_time = detection['timestamp']
            time_diff = abs(attack_time - detection_time)
            
            # Higher confidence for detections within 60 seconds
            if time_diff <= 60:
                confidence += 0.3
                break
            elif time_diff <= 300:  # 5 minutes
                confidence += 0.1
                break
        
        return min(confidence, 1.0)
    
    def _analyze_coverage(self, correlations: List[CorrelationResult]) -> CoverageAnalysis:
        """Analyze detection coverage"""
        total_attacks = len(correlations)
        detected_attacks = sum(1 for corr in correlations if corr.detected)
        false_positives = sum(1 for corr in correlations if corr.false_positive)
        false_negatives = sum(1 for corr in correlations if not corr.detected)
        
        coverage_percentage = (detected_attacks / total_attacks * 100) if total_attacks > 0 else 0
        accuracy = ((detected_attacks - false_positives) / total_attacks * 100) if total_attacks > 0 else 0
        
        # Analyze MITRE technique coverage
        mitre_coverage = {}
        for corr in correlations:
            if corr.mitre_technique:
                if corr.mitre_technique not in mitre_coverage:
                    mitre_coverage[corr.mitre_technique] = {
                        'total': 0,
                        'detected': 0,
                        'coverage': 0.0
                    }
                
                mitre_coverage[corr.mitre_technique]['total'] += 1
                if corr.detected:
                    mitre_coverage[corr.mitre_technique]['detected'] += 1
        
        # Calculate coverage for each MITRE technique
        for technique in mitre_coverage:
            total = mitre_coverage[technique]['total']
            detected = mitre_coverage[technique]['detected']
            mitre_coverage[technique]['coverage'] = (detected / total * 100) if total > 0 else 0
        
        # Generate recommendations
        recommendations = []
        if coverage_percentage < 70:
            recommendations.append("Detection coverage is below 70%. Review detection rules and monitoring coverage.")
        if false_negatives > 0:
            recommendations.append(f"{false_negatives} attacks were not detected. Strengthen detection capabilities.")
        if false_positives > 0:
            recommendations.append(f"{false_positives} false positives detected. Fine-tune detection rules.")
        
        # Calculate overall score (0-100)
        score = (coverage_percentage * 0.6) + (accuracy * 0.4)
        
        return CoverageAnalysis(
            total_attacks=total_attacks,
            detected_attacks=detected_attacks,
            coverage_percentage=coverage_percentage,
            false_positives=false_positives,
            false_negatives=false_negatives,
            accuracy=accuracy,
            mitre_coverage=mitre_coverage,
            recommendations=recommendations,
            score=score
        )
    
    def generate_report(self, results: Dict[str, Any], format: str = 'html') -> str:
        """Generate a report in the specified format"""
        if format == 'json':
            return json.dumps(results, indent=2, default=str)
        elif format == 'csv':
            return self._generate_csv_report(results)
        elif format == 'html':
            return self._generate_html_report(results)
        elif format == 'pdf':
            return self._generate_pdf_report(results)
        else:
            raise ValueError(f"Unsupported report format: {format}")
    
    def _generate_csv_report(self, results: Dict[str, Any]) -> str:
        """Generate CSV report"""
        # Create correlation data
        correlations = results['purple_logic']['correlations']
        
        if not correlations:
            return "No correlation data available"
        
        # Convert to DataFrame
        df = pd.DataFrame(correlations)
        
        # Add coverage summary
        coverage = results['purple_logic']['coverage']
        summary_data = {
            'metric': ['Total Attacks', 'Detected Attacks', 'Coverage %', 'Score'],
            'value': [
                coverage['total_attacks'],
                coverage['detected_attacks'],
                f"{coverage['coverage_percentage']:.1f}",
                f"{coverage['score']:.1f}"
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        
        # Combine data
        output = f"Purple Team Report - {results['scenario_name']}\n"
        output += f"Execution Time: {results['execution_time']}\n\n"
        output += "Coverage Summary:\n"
        output += summary_df.to_csv(index=False)
        output += "\n\nCorrelation Details:\n"
        output += df.to_csv(index=False)
        
        return output
    
    def _generate_html_report(self, results: Dict[str, Any]) -> str:
        """Generate HTML report"""
        template_str = """
<!DOCTYPE html>
<html>
<head>
    <title>Purple Team Report - {{ scenario_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; }
        .metric { display: inline-block; margin: 10px; padding: 10px; background-color: #e8f4f8; border-radius: 5px; }
        .score { font-size: 24px; font-weight: bold; color: #2c5aa0; }
        .coverage { font-size: 20px; color: #28a745; }
        .warning { color: #dc3545; }
        .success { color: #28a745; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .detected { background-color: #d4edda; }
        .not-detected { background-color: #f8d7da; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Purple Team Report</h1>
        <h2>{{ scenario_name }}</h2>
        <p>Execution Time: {{ execution_time }}</p>
    </div>
    
    <div class="section">
        <h3>Coverage Summary</h3>
        <div class="metric">
            <div class="score">{{ "%.1f"|format(coverage.score) }}/100</div>
            <div>Overall Score</div>
        </div>
        <div class="metric">
            <div class="coverage">{{ "%.1f"|format(coverage.coverage_percentage) }}%</div>
            <div>Detection Coverage</div>
        </div>
        <div class="metric">
            <div>{{ coverage.total_attacks }}</div>
            <div>Total Attacks</div>
        </div>
        <div class="metric">
            <div>{{ coverage.detected_attacks }}</div>
            <div>Detected Attacks</div>
        </div>
    </div>
    
    <div class="section">
        <h3>Correlation Results</h3>
        <table>
            <tr>
                <th>Attack Technique</th>
                <th>Expected Detection</th>
                <th>Actual Detection</th>
                <th>Detected</th>
                <th>MITRE Technique</th>
                <th>Confidence</th>
            </tr>
            {% for corr in correlations %}
            <tr class="{{ 'detected' if corr.detected else 'not-detected' }}">
                <td>{{ corr.attack_technique }}</td>
                <td>{{ corr.expected_detection }}</td>
                <td>{{ corr.actual_detection or 'None' }}</td>
                <td>{{ 'Yes' if corr.detected else 'No' }}</td>
                <td>{{ corr.mitre_technique or 'N/A' }}</td>
                <td>{{ "%.1f"|format(corr.confidence * 100) }}%</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    
    {% if coverage.recommendations %}
    <div class="section">
        <h3>Recommendations</h3>
        <ul>
            {% for rec in coverage.recommendations %}
            <li class="warning">{{ rec }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}
</body>
</html>
        """
        
        template = Template(template_str)
        return template.render(
            scenario_name=results['scenario_name'],
            execution_time=results['execution_time'],
            coverage=results['purple_logic']['coverage'],
            correlations=results['purple_logic']['correlations']
        )
    
    def _generate_pdf_report(self, results: Dict[str, Any]) -> str:
        """Generate PDF report (placeholder)"""
        # This would use a library like reportlab or weasyprint
        # For now, return HTML that can be converted to PDF
        return self._generate_html_report(results)
    
    def _correlation_to_dict(self, correlation: CorrelationResult) -> Dict[str, Any]:
        """Convert correlation result to dictionary"""
        return {
            'attack_technique': correlation.attack_technique,
            'expected_detection': correlation.expected_detection,
            'actual_detection': correlation.actual_detection,
            'detected': correlation.detected,
            'detection_time': correlation.detection_time,
            'false_positive': correlation.false_positive,
            'false_negative': correlation.false_negative,
            'mitre_technique': correlation.mitre_technique,
            'confidence': correlation.confidence,
            'details': correlation.details
        }
    
    def _coverage_to_dict(self, coverage: CoverageAnalysis) -> Dict[str, Any]:
        """Convert coverage analysis to dictionary"""
        return {
            'total_attacks': coverage.total_attacks,
            'detected_attacks': coverage.detected_attacks,
            'coverage_percentage': coverage.coverage_percentage,
            'false_positives': coverage.false_positives,
            'false_negatives': coverage.false_negatives,
            'accuracy': coverage.accuracy,
            'mitre_coverage': coverage.mitre_coverage,
            'recommendations': coverage.recommendations,
            'score': coverage.score
        }
