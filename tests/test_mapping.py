################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.01
#
# This script tests the mapping API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import unittest
from unittest.mock import MagicMock
from flask import Flask, jsonify
import sys
import os
import pytest
from app import create_app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes.mapping import bp

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
        self.app.config['MAP_LIST'] = [1, 2, 3]  # List of map IDs
        
        # Set up mock responses for get_map
        self.mock_robot.get_map.side_effect = lambda map_id: {
            'data': f'map{map_id}',
        }
        
        # Initialize MAP_DATA using the mock robot
        self.app.config['MAP_DATA'] = {
            map_id: self.mock_robot.get_map(map_id) for map_id in self.app.config['MAP_LIST']
        }
        
        self.app.config['CURR_MAP_ID'] = 1
        self.app.config['ROBOT'] = self.mock_robot

    def test_get_map_list(self):
        response = self.client.get('/api/getml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"map_list": [1, 2, 3]})

    def test_get_map_list_no_map_list(self):
        self.app.config['MAP_LIST'] = None
        response = self.client.get('/api/getml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"map_list": None})

    def test_get_compressed_map_data_same_map_id(self):
        response = self.client.get('/api/getmap/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"map_id": 1, "map_data": self.app.config['MAP_DATA'][1]})

    def test_get_compressed_map_data_invalid_map_id(self):
        response = self.client.get('/api/getmap/99')
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.json)

    def test_save_markers_success(self):
        test_data = {
            "map_id": 1,
            "markers": [{"id": 1, "position": [0, 0]}]
        }
        response = self.client.post('/api/save-markers', json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "map_id": 1,
            "markers": [{"id": 1, "position": [0, 0]}]
        })

    def test_save_markers_missing_map_id(self):
        test_data = {
            "markers": [{"id": 1, "position": [0, 0]}]
        }
        response = self.client.post('/api/save-markers', json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.json)

    def test_save_markers_invalid_json(self):
        response = self.client.post('/api/save-markers', data='invalid json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.json)

    def test_load_markers_success(self):
        # First save some markers
        test_data = {
            "map_id": 1,
            "markers": [{"id": 1, "position": [0, 0]}]
        }
        self.client.post('/api/save-markers', json=test_data)
        
        # Then load them
        response = self.client.get('/api/load-markers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "map_id": 1,
            "markers": [{"id": 1, "position": [0, 0]}]
        })

    def test_load_markers_empty(self):
        response = self.client.get('/api/load-markers/999')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "map_id": 999,
            "markers": []
        })

if __name__ == '__main__':
    unittest.main()
