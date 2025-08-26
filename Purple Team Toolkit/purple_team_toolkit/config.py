"""
Configuration management for Purple Team Toolkit
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

@dataclass
class Config:
    """Configuration class for Purple Team Toolkit"""
    
    # Safety settings
    sandbox_mode: bool = True
    rate_limiting: bool = True
    confirmation_required: bool = True
    full_audit_logging: bool = True
    
    # Logging settings
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # Output settings
    output_directory: str = "reports/"
    plugins_directory: str = "plugins/"
    
    # Network settings
    default_timeout: int = 30
    max_retries: int = 3
    
    # Red Team settings
    red_team_modules: Dict[str, Any] = field(default_factory=dict)
    
    # Blue Team settings
    blue_team_modules: Dict[str, Any] = field(default_factory=dict)
    
    # Purple Logic settings
    correlation_rules: Dict[str, Any] = field(default_factory=dict)
    
    # MITRE ATT&CK settings
    mitre_attack_mapping: bool = True
    attack_framework_version: str = "14.1"
    
    @classmethod
    def from_file(cls, config_path: str) -> 'Config':
        """Load configuration from file"""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
        
        return cls(**data)
    
    @classmethod
    def default(cls) -> 'Config':
        """Create default configuration"""
        return cls()
    
    def save(self, config_path: str):
        """Save configuration to file"""
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'sandbox_mode': self.sandbox_mode,
            'rate_limiting': self.rate_limiting,
            'confirmation_required': self.confirmation_required,
            'full_audit_logging': self.full_audit_logging,
            'log_level': self.log_level,
            'log_file': self.log_file,
            'output_directory': self.output_directory,
            'plugins_directory': self.plugins_directory,
            'default_timeout': self.default_timeout,
            'max_retries': self.max_retries,
            'red_team_modules': self.red_team_modules,
            'blue_team_modules': self.blue_team_modules,
            'correlation_rules': self.correlation_rules,
            'mitre_attack_mapping': self.mitre_attack_mapping,
            'attack_framework_version': self.attack_framework_version
        }
        
        with open(config_path, 'w') as f:
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                yaml.dump(data, f, default_flow_style=False, indent=2)
            else:
                json.dump(data, f, indent=2)
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.log_file) if self.log_file else logging.NullHandler()
            ]
        )
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        errors = []
        
        # Check required directories
        if not Path(self.output_directory).exists():
            try:
                Path(self.output_directory).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create output directory: {e}")
        
        if not Path(self.plugins_directory).exists():
            try:
                Path(self.plugins_directory).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create plugins directory: {e}")
        
        # Validate log level
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level.upper() not in valid_log_levels:
            errors.append(f"Invalid log level: {self.log_level}")
        
        # Validate timeouts
        if self.default_timeout <= 0:
            errors.append("Default timeout must be positive")
        
        if self.max_retries < 0:
            errors.append("Max retries cannot be negative")
        
        if errors:
            raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")
        
        return True
