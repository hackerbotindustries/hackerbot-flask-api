################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.05.24
#
# This script tests the arm API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from app.routers.arm import router  # Update to correct path if different

@pytest.fixture
def app_with_mock_robot():
    app = FastAPI()
    mock_robot = MagicMock()
    mock_robot.core.ping.return_value = "pong"
    mock_robot.core.version.return_value = "1.0.0"
    mock_robot.get_error.return_value = "simulated error"
    app.include_router(router)
    app.state.robot = mock_robot
    return app, mock_robot

@pytest.fixture
def client(app_with_mock_robot):
    app, _ = app_with_mock_robot
    return TestClient(app)

# ---------- /arm/gripper ----------

def test_gripper_open(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.arm.gripper.open.return_value = "open"
    response = client.post("/arm/gripper", json={"method": "open"})
    assert response.status_code == 200
    assert response.json() == {"response": "open"}

# ---------- /arm ----------

def test_arm_move_joint(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.arm.move_joint.return_value = "moved"
    response = client.post("/arm", json={"method": "move-joint", "joint": 1, "angle": 45.0, "speed": 1.0})
    assert response.status_code == 200
    assert response.json() == {"response": "moved"}
