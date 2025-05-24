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
# This script tests the core API endpoints.
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
from app.routers.core import router  # Update to correct path if different

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
    response = client.post("/core", json={"method": "settings", "json_responses": True, "tofs_enabled": True})
    assert response.status_code == 200
    assert response.json() == {"response": True}

def test_core_missing_method(client):
    response = client.post("/core", json={})
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("Field required" in err["msg"] for err in detail)

def test_core_invalid_method(client):
    response = client.post("/core", json={"method": "unknown"})
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("Input should be" in err["msg"] for err in detail)

# ---------- /core/version ----------

def test_core_version_success(client, app_with_mock_robot):
    response = client.get("/core/version")
    assert response.status_code == 200
    assert response.json() == {"response": "1.0.0"}