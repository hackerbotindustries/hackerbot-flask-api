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
# This script tests the base API endpoints.
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
from app.routers.base import router  # Update to correct path if different

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
    errors = response.json()["detail"]
    assert any("Input should be" in err["msg"] for err in errors)

# ---------- /base/status ----------

def test_base_status(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.base.status.return_value = {"state": "idle"}
    response = client.get("/base/status")
    assert response.status_code == 200
    assert response.json() == {"response": {"state": "idle"}}
