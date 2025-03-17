import unittest
from unittest.mock import MagicMock
from flask import Flask, jsonify
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes.mapping import bp  # Adjust import path based on your project structure

class TestMappingDataAPI(unittest.TestCase):

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
        self.app.config['MAP_LIST'] = ["map1", "map2", "map3"]
        self.app.config['MAP_DATA'] = {"map1": "data1", "map2": "data2"}
        self.app.config['CURR_MAP_ID'] = 1
        self.app.config['ROBOT'] = self.mock_robot

    def test_get_map_list(self):
        # Test /api/getml route
        response = self.client.get('/api/getml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"map_list": ["map1", "map2", "map3"]})

    def test_get_compressed_map_data_same_map_id(self):
        # Test /api/getmap/<selected_map_id> route with the same map_id
        response = self.client.get('/api/getmap/1')  # same as CURR_MAP_ID
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"map_id": 1, "map_data": {"map1": "data1", "map2": "data2"}})

    def test_get_compressed_map_data_different_map_id(self):
        # Test /api/getmap/<selected_map_id> route with a different map_id
        self.mock_robot.get_map.return_value = {"map3": "data3"}  # Mock the robot to return map3 data
        
        # New map_id is different from CURR_MAP_ID, so the map should be fetched
        response = self.client.get('/api/getmap/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"map_id": 2, "map_data": {"map3": "data3"}})
        
        # Verify the robot's `get_map` method was called with the correct map_id
        self.mock_robot.get_map.assert_called_once_with(2)
        self.assertEqual(self.app.config['CURR_MAP_ID'], 2)  # Verify that the CURR_MAP_ID was updated

    def test_get_compressed_map_data_invalid_map_id(self):
        # Test /api/getmap/<selected_map_id> route with invalid map_id
        # Simulate an invalid or non-existent map_id scenario (you can adjust based on your application)
        self.mock_robot.get_map.return_value = None  # Let's say the robot fails to return map data
        
        response = self.client.get('/api/getmap/99')  # Assuming map 99 doesn't exist
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"map_id": 99, "map_data": None})

if __name__ == '__main__':
    unittest.main()
