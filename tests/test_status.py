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
# This script tests the status API endpoints.
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
from unittest.mock import MagicMock
from app.routers.status import router 

@pytest.fixture
def app_with_mock_robot():
    app = FastAPI()
    mock_robot = MagicMock()
    app.include_router(router)
    app.state.robot = mock_robot
    return app, mock_robot

@pytest.fixture
def client(app_with_mock_robot):
    app, _ = app_with_mock_robot
    return TestClient(app)

# ------------------- /status -------------------

def test_status_with_current_action(client, app_with_mock_robot):
    app, mock_robot = app_with_mock_robot
    mock_robot.get_current_action.return_value = "moving"
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "moving"}

def test_status_with_no_current_action(client, app_with_mock_robot):
    app, mock_robot = app_with_mock_robot
    mock_robot.get_current_action.return_value = None
    response = client.get("/status")
    assert response.status_code == 204
    assert response.json() == {"status": None, "warning": "No current action available"}

def test_status_with_missing_robot(client):
    app = FastAPI()
    app.include_router(router)
    test_client = TestClient(app)
    response = test_client.get("/status")
    assert response.status_code == 500
    assert response.json()["detail"] == "Robot is not initialized in app state"

def test_status_with_exception(client, app_with_mock_robot):
    app, mock_robot = app_with_mock_robot
    mock_robot.get_current_action.side_effect = Exception("Unexpected error")
    response = client.get("/status")
    assert response.status_code == 500
    assert "Failed to retrieve status" in response.json()["error"]

# ------------------- /error -------------------

def test_error_with_existing_error(client, app_with_mock_robot):
    app, mock_robot = app_with_mock_robot
    mock_robot.get_error.return_value = "Motor overload"
    response = client.get("/error")
    assert response.status_code == 200
    assert response.json() == {"error": "Motor overload"}

def test_error_with_no_error(client, app_with_mock_robot):
    app, mock_robot = app_with_mock_robot
    mock_robot.get_error.return_value = None
    response = client.get("/error")
    assert response.status_code == 200
    assert response.json() == {"message": "None"}

def test_error_with_missing_robot(client):
    app = FastAPI()
    app.include_router(router)
    test_client = TestClient(app)
    response = test_client.get("/error")
    assert response.status_code == 500
    assert response.json()["detail"] == "Robot is not initialized in app state"

def test_error_with_exception(client, app_with_mock_robot):
    app, mock_robot = app_with_mock_robot
    mock_robot.get_error.side_effect = Exception("Internal fault")
    response = client.get("/error")
    assert response.status_code == 500
    assert "Failed to retrieve error state" in response.json()["error"]
