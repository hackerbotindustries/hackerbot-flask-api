import unittest
from unittest.mock import MagicMock
from flask import Flask, jsonify, current_app
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes.status import bp  # Import your Blueprint containing the routes

class TestStatusAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a Flask app for testing
        cls.app = Flask(__name__)
        cls.app.register_blueprint(bp)  # Register the blueprint
        cls.client = cls.app.test_client()
        cls.app.testing = True

    def setUp(self):
        # Mock the robot object inside the app config for each test
        self.mock_robot = MagicMock()
        self.app.config['ROBOT'] = self.mock_robot

    def test_get_status_success(self):
        # Mock the return value of robot.get_current_action()
        self.mock_robot.get_current_action.return_value = "Idle"

        response = self.client.get('/api/status')

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the response JSON contains the expected status
        self.assertEqual(response.json, {"status": "Idle"})

    def test_get_status_failure(self):
        # Mock the return value of robot.get_current_action() as None or an error
        self.mock_robot.get_current_action.return_value = None

        response = self.client.get('/api/status')

        # Check that the response status code is 200 even in case of None
        # Since we still get a response, even if it's an empty one
        self.assertEqual(response.status_code, 200)

        # Check that the response JSON contains a None or empty status
        self.assertEqual(response.json, {"status": None})

    def test_get_error_success(self):
        # Mock the return value of robot.get_error()
        self.mock_robot.get_error.return_value = "No error"

        response = self.client.get('/api/error')

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the response JSON contains the expected error message
        self.assertEqual(response.json, {"error": "No error"})

    def test_get_error_failure(self):
        # Mock the return value of robot.get_error() as None or an error
        self.mock_robot.get_error.return_value = None

        response = self.client.get('/api/error')

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the response JSON contains a None or empty error message
        self.assertEqual(response.json, {"error": None})

if __name__ == '__main__':
    unittest.main()
