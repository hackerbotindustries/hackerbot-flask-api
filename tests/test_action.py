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


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from app.routers.action import router  # Update to correct path if different

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

# ---------- /core ----------

def test_core_ping(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    response = client.post("/core", json={"method": "ping"})
    assert response.status_code == 200
    assert response.json() == {"response": "pong"}

def test_core_settings(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.set_json_mode.return_value = True
    robot.set_TOFs.return_value = True
    response = client.post("/core", json={"method": "settings", "json-responses": True, "tofs-enabled": True})
    assert response.status_code == 200
    assert response.json() == {"response": True}

def test_core_missing_method(client):
    response = client.post("/core", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "Missing method"

def test_core_invalid_method(client):
    response = client.post("/core", json={"method": "unknown"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid method"

# ---------- /core/version ----------

def test_core_version_success(client, app_with_mock_robot):
    response = client.get("/core/version")
    assert response.status_code == 200
    assert response.json() == {"response": "1.0.0"}

# ---------- /base ----------

def test_base_drive_command(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.base.drive.return_value = "driving"
    payload = {"method": "drive", "linear_velocity": 0.5, "angle_velocity": 0.1}
    response = client.post("/base", json=payload)
    assert response.status_code == 200
    assert response.json() == {"response": "driving"}

def test_base_invalid_method(client):
    response = client.post("/base", json={"method": "fly"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid method"

# ---------- /base/status ----------

def test_base_status(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.base.status.return_value = {"state": "idle"}
    response = client.get("/base/status")
    assert response.status_code == 200
    assert response.json() == {"response": {"state": "idle"}}

# ---------- /head ----------

def test_head_put_idle_mode(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.head.set_idle_mode.return_value = True
    response = client.put("/head", json={"idle-mode": True})
    assert response.status_code == 200
    assert response.json() == {"response": True}

def test_head_post_look(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.head.look.return_value = "looking"
    response = client.post("/head", json={"method": "look", "yaw": 1.0, "pitch": 0.5, "speed": 1.0})
    assert response.status_code == 200
    assert response.json() == {"response": "looking"}

def test_head_post_gaze(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.head.eyes.gaze.return_value = "gazing"
    response = client.post("/head", json={"method": "gaze", "x": 100, "y": 200})
    assert response.status_code == 200
    assert response.json() == {"response": "gazing"}

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
