################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.11
#
# This script tests the action API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import unittest
from unittest.mock import MagicMock
from flask import Flask
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes.action import bp

class TestActionAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(bp)
        cls.app.testing = True
        cls.client = cls.app.test_client()

    def setUp(self):
        self.mock_robot = MagicMock()
        self.mock_robot._controller.set_json_mode.return_value = True
        self.mock_robot._controller.set_tof_mode.return_value = True
        self.mock_robot._controller.set_idle_mode.return_value = True
        self.mock_robot.core.ping.return_value = 'pong'
        self.mock_robot.core.version.return_value = '1.0.0'
        self.mock_robot.base.initialize.return_value = 'initialized'
        self.mock_robot.base.set_mode.return_value = 'mode set'
        self.mock_robot.base.start.return_value = 'started'
        self.mock_robot.base.status.return_value = 'ok'
        self.mock_robot.base.drive.return_value = 'driving'
        self.mock_robot.base.maps.position.return_value = {'x': 1, 'y': 2, 'angle': 90}
        self.mock_robot.base.maps.goto.return_value = 'arrived'
        self.mock_robot.base.get_map.return_value = {'map_id': '123'}
        self.mock_robot.base.list_maps.return_value = ['map1', 'map2']
        self.mock_robot.head.look.return_value = 'looking'
        self.mock_robot.head.eyes.gaze.return_value = 'gazing'
        # self.mock_robot.head.get_position.return_value = {'yaw': 0.5, 'pitch': 0.3}
        self.mock_robot.arm.gripper.calibrate.return_value = 'calibrated'
        self.mock_robot.arm.gripper.open.return_value = 'opened'
        self.mock_robot.arm.gripper.close.return_value = 'closed'
        self.mock_robot.arm.move_joint.return_value = 'joint moved'
        self.mock_robot.arm.move_joints.return_value = 'joints moved'
        # self.mock_robot.arm.get_position.return_value = [0.1, 0.2, 0.3]
        self.mock_robot.get_error.return_value = 'Some error'
        self.app = self.__class__.app
        self.app.config['ROBOT'] = self.mock_robot

    def test_core_ping(self):
        response = self.client.post('/api/v1/core', json={'method': 'ping'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'pong'})

    def test_core_version(self):
        response = self.client.get('/api/v1/core/version')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': '1.0.0'})

    def test_core_settings_json_mode(self):
        self.mock_robot.set_json_mode.return_value = True
        response = self.client.post('/api/v1/core', json={'method': 'settings', 'json-responses': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': True})

    def test_core_settings_tof_mode(self):
        self.mock_robot.set_TOFs.return_value = True
        response = self.client.post('/api/v1/core', json={'method': 'settings', 'tofs-enabled': False})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['response'])

    def test_head_idle_mode_true(self):
        self.mock_robot.head.set_idle_mode.return_value = True
        response = self.client.put('/api/v1/head', json={'idle-mode': True})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['response'])

    def test_head_look(self):
        response = self.client.post('/api/v1/head', json={'method': 'look', 'yaw': 1.0, 'pitch': 2.0, 'speed': 0.5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'looking')

    def test_head_gaze(self):
        response = self.client.post('/api/v1/head', json={'method': 'gaze', 'x': 3.0, 'y': 4.0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'gazing')

    # def test_head_position(self):
    #     response = self.client.get('/api/v1/head/position')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('yaw', response.json['response'])

    def test_base_initialize(self):
        response = self.client.post('/api/v1/base', json={'method': 'initialize'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'initialized')

    def test_base_mode(self):
        response = self.client.post('/api/v1/base', json={'method': 'mode', 'mode_id': 'explore'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'mode set')

    def test_base_speak_valid(self):
        response = self.client.post('/api/v1/base', json={'method': 'speak', 'text': 'Hello Test World!', "model_src": "en_US-amy-low"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'mode set')

    def test_base_speak_invalid_model(self):
        response = self.client.post('/api/v1/base', json={'method': 'speak', 'text': 'Hello Test World!', "model_src": "hello"})
        self.assertEqual(response.status_code, 422)

    def test_base_speak_invalid_missing_text(self):
        response = self.client.post('/api/v1/base', json={'method': 'speak', "model_src": "en_US-amy-low"})
        self.assertEqual(response.status_code, 422)

    def test_base_status(self):
        response = self.client.get('/api/v1/base/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'ok')

    def test_base_drive(self):
        response = self.client.post('/api/v1/base/actions', json={'linear_velocity': 1.0, 'angle_velocity': 0.2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'driving')

    def test_base_position(self):
        response = self.client.get('/api/v1/base/maps/position')
        self.assertEqual(response.status_code, 200)
        self.assertIn('x', response.json['response'])

    def test_base_goto(self):
        response = self.client.post('/api/v1/base/maps', json={'method':'goto','x': 1.0, 'y': 2.0, 'angle': 90, 'speed': 0.5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'arrived')

    def test_gripper_calibrate(self):
        response = self.client.post('/api/v1/arm/gripper', json={'method': 'calibrate'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'calibrated')

    def test_gripper_open(self):
        response = self.client.post('/api/v1/arm/gripper', json={'method': 'open'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'opened')

    def test_gripper_close(self):
        response = self.client.post('/api/v1/arm/gripper', json={'method': 'close'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'closed')

    def test_arm_move_joint(self):
        response = self.client.post('/api/v1/arm', json={'method': 'move-joint', 'joint': 'shoulder', 'angle': 30.0, 'speed': 0.5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'joint moved')

    def test_arm_move_joints(self):
        response = self.client.post('/api/v1/arm', json={'method': 'move-joints', 'angles': [0.1, 0.2], 'speed': 0.5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'joints moved')

    # def test_arm_position(self):
    #     response = self.client.get('/api/v1/arm/position')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.json['response'], list)

if __name__ == '__main__':
    unittest.main()
