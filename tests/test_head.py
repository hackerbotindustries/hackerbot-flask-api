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
# This script tests the head API endpoints.
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
from app.routers.head import router  # Update to correct path if different

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

# ---------- /head ----------

def test_head_put_idle_mode(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.head.set_idle_mode.return_value = True
    response = client.put("/head", json={"idle_mode": True}) 
    assert response.status_code == 200
    assert response.json() == {"response": True}

def test_head_put_idle_mode_invalid(client):
    response = client.put("/head", json={})  # missing idle_mode
    assert response.status_code == 422

def test_head_post_look(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.head.look.return_value = "looking"
    response = client.post("/head", json={"method": "look", "pan": 1.0, "tilt": 0.5, "speed": 1.0})
    assert response.status_code == 200
    assert response.json() == {"response": "looking"}

def test_head_post_gaze(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.head.eyes.gaze.return_value = "gazing"
    response = client.post("/head", json={"method": "gaze", "x": 100, "y": 200})
    assert response.status_code == 200
    assert response.json() == {"response": "gazing"}