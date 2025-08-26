"""
Unit tests for Red Team modules
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import time

from purple_team_toolkit.red_team.modules import (
    ReconnaissanceModule, 
    ExploitationModule, 
    PostExploitationModule,
    AttackResult
)
from purple_team_toolkit.red_team.payloads import PayloadManager, Payload

class TestReconnaissanceModule(unittest.TestCase):
    """Test reconnaissance module functionality"""
    
    def setUp(self):
        self.config = {'nmap_path': '/usr/bin/nmap'}
        self.recon_module = ReconnaissanceModule(self.config)
    
    @patch('purple_team_toolkit.red_team.modules.nmap.PortScanner')
    def test_nmap_scan_success(self, mock_nmap):
        """Test successful nmap scan"""
        # Mock nmap results
        mock_scanner = Mock()
        mock_scanner.all_hosts.return_value = ['192.168.1.1']
        
        # Create a proper mock for the host object
        mock_host = Mock()
        mock_host.state.return_value = 'up'
        mock_host.all_protocols.return_value = ['tcp']
        
        # Create a proper mock for the tcp protocol
        mock_tcp = Mock()
        mock_tcp.keys.return_value = [80, 443]
        
        # Set up the mock to return the port data
        port_data = {
            80: {'state': 'open', 'name': 'http', 'version': '1.1', 'product': 'nginx'},
            443: {'state': 'open', 'name': 'https', 'version': '1.1', 'product': 'nginx'}
        }
        mock_tcp.__getitem__ = Mock(side_effect=lambda key: port_data[key])
        
        # Set up the host mock to return the tcp protocol
        mock_host.__getitem__ = Mock(side_effect=lambda key: {'tcp': mock_tcp}[key])
        
        # Set up the scanner mock to return the host
        mock_scanner.__getitem__ = Mock(side_effect=lambda key: {'192.168.1.1': mock_host}[key])
        mock_scanner.scanstats.return_value = {'timestr': '0.05s'}
        mock_nmap.return_value = mock_scanner
        
        # Re-initialize the module with the mock
        self.recon_module.nm = mock_scanner
        self.recon_module.nmap_available = True
        
        result = self.recon_module.nmap_scan('192.168.1.1', 'basic')
        
        self.assertIsInstance(result, AttackResult)
        self.assertTrue(result.success)
        self.assertEqual(result.technique, 'nmap_scan')
        self.assertEqual(result.target, '192.168.1.1')
        self.assertEqual(result.mitre_technique, 'T1046')
    
    @patch('purple_team_toolkit.red_team.modules.nmap.PortScanner')
    def test_nmap_scan_failure(self, mock_nmap):
        """Test nmap scan failure"""
        mock_scanner = Mock()
        mock_scanner.scan.side_effect = Exception("Nmap not found")
        mock_nmap.return_value = mock_scanner
        
        result = self.recon_module.nmap_scan('192.168.1.1', 'basic')
        
        self.assertIsInstance(result, AttackResult)
        self.assertFalse(result.success)
        self.assertIn('error', result.data)
    
    @patch('purple_team_toolkit.red_team.modules.dns.resolver.resolve')
    def test_dns_enumeration_success(self, mock_resolve):
        """Test successful DNS enumeration"""
        # Mock DNS responses
        mock_resolve.side_effect = [
            ['192.168.1.1'],  # A record
            ['2001:db8::1'],  # AAAA record
            ['mail.example.com'],  # MX record
            ['ns1.example.com', 'ns2.example.com'],  # NS record
            ['v=spf1 include:_spf.example.com ~all']  # TXT record
        ]
        
        result = self.recon_module.dns_enumeration('example.com')
        
        self.assertIsInstance(result, AttackResult)
        self.assertTrue(result.success)
        self.assertEqual(result.technique, 'dns_enumeration')
        self.assertEqual(result.target, 'example.com')
        self.assertEqual(result.mitre_technique, 'T1590')
    
    @patch('purple_team_toolkit.red_team.modules.whois')
    def test_whois_lookup_success(self, mock_whois):
        """Test successful WHOIS lookup"""
        # Mock WHOIS response
        mock_whois_data = Mock()
        mock_whois_data.domain_name = 'example.com'
        mock_whois_data.registrar = 'Example Registrar'
        mock_whois_data.creation_date = '2000-01-01'
        mock_whois_data.expiration_date = '2025-01-01'
        mock_whois_data.updated_date = '2024-01-01'
        mock_whois_data.name_servers = ['ns1.example.com', 'ns2.example.com']
        mock_whois_data.status = 'active'
        mock_whois_data.emails = ['admin@example.com']
        mock_whois.return_value = mock_whois_data
        
        result = self.recon_module.whois_lookup('example.com')
        
        self.assertIsInstance(result, AttackResult)
        self.assertTrue(result.success)
        self.assertEqual(result.technique, 'whois_lookup')
        self.assertEqual(result.target, 'example.com')
        self.assertEqual(result.mitre_technique, 'T1590')

class TestExploitationModule(unittest.TestCase):
    """Test exploitation module functionality"""
    
    def setUp(self):
        self.config = {}
        self.exploitation_module = ExploitationModule(self.config)
    
    @patch('purple_team_toolkit.red_team.modules.requests.get')
    def test_web_fuzzing_success(self, mock_get):
        """Test successful web fuzzing"""
        # Mock HTTP responses
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html>Found</html>'
        mock_get.return_value = mock_response
        
        result = self.exploitation_module.web_fuzzing('http://example.com')
        
        self.assertIsInstance(result, AttackResult)
        self.assertTrue(result.success)
        self.assertEqual(result.technique, 'web_fuzzing')
        self.assertEqual(result.target, 'http://example.com')
        self.assertEqual(result.mitre_technique, 'T1590')
    
    @patch('purple_team_toolkit.red_team.modules.socket.socket')
    def test_port_scan_success(self, mock_socket):
        """Test successful port scan"""
        # Mock socket connection
        mock_sock = Mock()
        mock_sock.connect_ex.return_value = 0  # Port open
        mock_socket.return_value = mock_sock
        
        result = self.exploitation_module.port_scan('192.168.1.1', [80, 443])
        
        self.assertIsInstance(result, AttackResult)
        self.assertTrue(result.success)
        self.assertEqual(result.technique, 'port_scan')
        self.assertEqual(result.target, '192.168.1.1')
        self.assertEqual(result.mitre_technique, 'T1046')

class TestPostExploitationModule(unittest.TestCase):
    """Test post-exploitation module functionality"""
    
    def setUp(self):
        self.config = {}
        self.post_exploitation_module = PostExploitationModule(self.config)
    
    def test_lateral_movement_simulation(self):
        """Test lateral movement simulation"""
        result = self.post_exploitation_module.lateral_movement_simulation('192.168.1.100')
        
        self.assertIsInstance(result, AttackResult)
        self.assertTrue(result.success)
        self.assertEqual(result.technique, 'lateral_movement')
        self.assertEqual(result.target, '192.168.1.100')
        self.assertEqual(result.mitre_technique, 'T1021')
        self.assertIn('techniques_simulated', result.data)
    
    def test_persistence_simulation(self):
        """Test persistence simulation"""
        result = self.post_exploitation_module.persistence_simulation('192.168.1.100')
        
        self.assertIsInstance(result, AttackResult)
        self.assertTrue(result.success)
        self.assertEqual(result.technique, 'persistence')
        self.assertEqual(result.target, '192.168.1.100')
        self.assertEqual(result.mitre_technique, 'T1053')
        self.assertIn('techniques_simulated', result.data)

class TestPayloadManager(unittest.TestCase):
    """Test payload manager functionality"""
    
    def setUp(self):
        self.config = {}
        self.payload_manager = PayloadManager(self.config)
    
    def test_get_payload(self):
        """Test getting a payload by name"""
        payload = self.payload_manager.get_payload('SQL Injection Test')
        
        self.assertIsInstance(payload, Payload)
        self.assertEqual(payload.name, 'SQL Injection Test')
        self.assertEqual(payload.type, 'web')
        self.assertEqual(payload.mitre_technique, 'T1190')
    
    def test_get_payloads_by_type(self):
        """Test getting payloads by type"""
        web_payloads = self.payload_manager.get_payloads_by_type('web')
        
        self.assertIsInstance(web_payloads, list)
        for payload in web_payloads:
            self.assertEqual(payload.type, 'web')
    
    def test_get_safe_payloads(self):
        """Test getting safe payloads"""
        safe_payloads = self.payload_manager.get_safe_payloads()
        
        self.assertIsInstance(safe_payloads, list)
        for payload in safe_payloads:
            self.assertTrue(payload.sandbox_safe)
    
    def test_generate_custom_payload(self):
        """Test generating custom payload"""
        payload = self.payload_manager.generate_custom_payload(
            'web', 
            attack_type='xss', 
            target='test'
        )
        
        self.assertIsInstance(payload, Payload)
        self.assertEqual(payload.type, 'web')
        self.assertIn('script', payload.content)
    
    def test_list_payloads(self):
        """Test listing all payloads"""
        payloads = self.payload_manager.list_payloads()
        
        self.assertIsInstance(payloads, list)
        self.assertGreater(len(payloads), 0)
        
        for payload_info in payloads:
            self.assertIn('name', payload_info)
            self.assertIn('type', payload_info)
            self.assertIn('description', payload_info)

if __name__ == '__main__':
    unittest.main()
