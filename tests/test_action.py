import unittest
from unittest.mock import MagicMock
from flask import Flask
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes.action import bp  # Adjust import path based on your project structure

class TestActionAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Flask app and register the Blueprint
        cls.app = Flask(__name__)
        cls.app.register_blueprint(bp)
        cls.client = cls.app.test_client()
        cls.app.testing = True

    def setUp(self):
        # Mock the current_app.config values for the tests
        self.mock_robot = MagicMock()
        self.app.config['ROBOT'] = self.mock_robot

    def test_ping_command_success(self):
        # Test /api/ping route when robot.get_ping() is successful
        self.mock_robot.get_ping.return_value = "true"
        
        response = self.client.get('/api/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': "true"})

    def test_ping_command_error(self):
        # Test /api/ping route when robot.get_ping() fails
        self.mock_robot.get_ping.return_value = None
        self.mock_robot.get_error.return_value = "Ping error"
        
        response = self.client.get('/api/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'error': "Ping error"})

    def test_version_command_success(self):
        # Test /api/version route when robot.get_versions() is successful
        self.mock_robot.get_versions.return_value = "1.0.0"
        
        response = self.client.get('/api/version/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': "1.0.0"})

    def test_version_command_error(self):
        # Test /api/version route when robot.get_versions() fails
        self.mock_robot.get_versions.return_value = None
        self.mock_robot.get_error.return_value = "Version error"
        
        response = self.client.get('/api/version/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'error': "Version error"})

    def test_stop_command_success(self):
        # Test /api/stop route when robot.stop_driver() is successful
        self.mock_robot.stop_driver.return_value = True
        
        response = self.client.get('/api/stop/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'STOP Command Successful'})

    def test_stop_command_error(self):
        # Test /api/stop route when robot.stop_driver() fails
        self.mock_robot.stop_driver.return_value = False
        self.mock_robot.get_error.return_value = "Stop error"
        
        response = self.client.get('/api/stop/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'error': "Stop error"})

    def test_machine_command_activate(self):
        # Test /api/machine/1 route to activate machine mode
        self.mock_robot.activate_machine_mode.return_value = True
        
        response = self.client.post('/api/machine/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'MACHINE Command Successful'})

    def test_machine_command_deactivate(self):
        # Test /api/machine/0 route to deactivate machine mode
        self.mock_robot.deactivate_machine_mode.return_value = True
        
        response = self.client.post('/api/machine/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'MACHINE Command Successful'})

    def test_machine_command_error(self):
        # Test /api/machine route when robot.get_error() is triggered
        self.mock_robot.activate_machine_mode.return_value = False
        self.mock_robot.get_error.return_value = "Machine error"
        
        response = self.client.post('/api/machine/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'error': "Machine error"})

    def test_init_command_success(self):
        # Test /api/init route when robot.init_driver() is successful
        self.mock_robot.init_driver.return_value = True
        
        response = self.client.get('/api/init/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'INIT Command Successful'})

    def test_init_command_error(self):
        # Test /api/init route when robot.init_driver() fails
        self.mock_robot.init_driver.return_value = False
        self.mock_robot.get_error.return_value = "Init error"
        
        response = self.client.get('/api/init/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'error': "Init error"})

    def test_goto_command_success(self):
        # Test /api/goto/<param> route when robot.goto_pos() is successful
        self.mock_robot.goto_pos.return_value = True
        
        response = self.client.post('/api/goto/1,2,90,10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'GOTO Command Successful'})

    def test_goto_command_error(self):
        # Test /api/goto/<param> route when robot.goto_pos() fails
        self.mock_robot.goto_pos.return_value = False
        self.mock_robot.get_error.return_value = "Goto error"
        
        response = self.client.post('/api/goto/1,2,90,10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'error': "Goto error"})

    def test_enter_command_success(self):
        # Test /api/enter route when robot.leave_base() is successful
        self.mock_robot.leave_base.return_value = True
        
        response = self.client.get('/api/enter/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'Enter Command Successful'})

    def test_enter_command_error(self):
        # Test /api/enter route when robot.leave_base() fails
        self.mock_robot.leave_base.return_value = False
        self.mock_robot.get_error.return_value = "Enter error"
        
        response = self.client.get('/api/enter/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'error': "Enter error"})

    def test_dock_command_success(self):
        # Test /api/dock route when robot.dock() is successful
        self.mock_robot.dock.return_value = True
        
        response = self.client.get('/api/dock/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'DOCK Command Successful'})

    def test_dock_command_error(self):
        # Test /api/dock route when robot.dock() fails
        self.mock_robot.dock.return_value = False
        self.mock_robot.get_error.return_value = "Dock error"
        
        response = self.client.get('/api/dock/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'error': "Dock error"})

    def test_quickmap_command_success(self):
        # Test /api/quickmap route when robot.quickmap() is successful
        self.mock_robot.quickmap.return_value = True
        
        response = self.client.get('/api/quickmap/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'QUICKMAP Command Successful'})

    def test_quickmap_command_error(self):
        # Test /api/quickmap route when robot.quickmap() fails
        self.mock_robot.quickmap.return_value = False
        self.mock_robot.get_error.return_value = "Quickmap error"
        
        response = self.client.get('/api/quickmap/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'error': "Quickmap error"})

if __name__ == '__main__':
    unittest.main()
