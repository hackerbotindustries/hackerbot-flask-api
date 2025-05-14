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

from app.routes.mapping import bp, map_data_db

class TestMappingDataAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(bp)
        cls.client = cls.app.test_client()
        cls.app.testing = True

    def setUp(self):
        self.mock_robot = MagicMock()
        self.app = self.__class__.app
        self.app.config['ROBOT'] = self.mock_robot

        # self.mock_robot.base.maps.fetch.side_effect = lambda map_id: {'data': f'map{map_id}'}

    def test_get_map_list(self):
        self.mock_robot.base.maps.list.return_value = [1, 2, 3]
        response = self.client.get('/api/v1/base/maps')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"map_list": [1, 2, 3]})

    def test_get_map_list_missing(self):
        self.mock_robot.base.maps.list.return_value = None
        self.app.config['MAP_LIST'] = None
        response = self.client.get('/api/v1/base/maps')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "No map list found"})

    def test_get_compressed_map_valid(self):
        self.mock_robot.base.maps.fetch.return_value = 'map1'
        response = self.client.get('/api/v1/base/maps/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "map_id": 1,
            "map_data": 'map1'
        })

    def test_get_compressed_map_invalid_id(self):
        self.mock_robot.base.maps.fetch.return_value = None
        response = self.client.get('/api/v1/base/maps/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Map data not found", response.json["error"])

    def test_get_compressed_map_robot_missing(self):
        del self.app.config['ROBOT']
        self.app.config['MAP_DATA'] = {}
        response = self.client.get('/api/v1/base/maps/1')
        self.assertEqual(response.status_code, 500)
        self.assertIn("Robot not configured", response.json["error"])

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
