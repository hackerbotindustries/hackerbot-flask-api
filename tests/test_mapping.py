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


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.routers.mapping import router, map_data_db, markers_db  # adjust path as needed

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

# ---------------------- GET /base/maps ----------------------

def test_base_goto_success(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.base.maps.goto.return_value = "navigating"
    payload = {"method": "goto", "x": 1.0, "y": 2.0, "angle": 0.0, "speed": 0.5}
    response = client.post("/base/maps", json=payload)
    assert response.status_code == 200
    assert response.json() == {"response": "navigating"}

def test_get_map_list_success(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.base.maps.list.return_value = [{"id": 1, "name": "Map A"}]

    response = client.get("/base/maps")
    assert response.status_code == 200
    assert response.json() == {"map_list": [{"id": 1, "name": "Map A"}]}

def test_get_map_list_none(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.base.maps.list.return_value = None

    response = client.get("/base/maps")
    assert response.status_code == 404
    assert response.json()["detail"] == "No map list found"

def test_get_map_list_robot_missing():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    response = client.get("/base/maps")
    assert response.status_code == 500
    assert response.json()["detail"] == "Robot is not initialized in app state"

# ---------------------- GET /base/maps/position ----------------------

def test_base_position_success(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.base.maps.position.return_value = {"x": 1, "y": 2, "theta": 90}

    response = client.get("/base/maps/position")
    assert response.status_code == 200
    assert response.json() == {"response": {"x": 1, "y": 2, "theta": 90}}

def test_base_position_failure(client, app_with_mock_robot):
    _, robot = app_with_mock_robot
    robot.base.maps.position.return_value = None
    robot.get_error.return_value = "Positioning system offline"

    response = client.get("/base/maps/position")
    assert response.status_code == 500
    assert response.json()["error"] == "Positioning system offline"

# ---------------------- GET /base/maps/{map_id} ----------------------

def test_get_compressed_map_data_from_robot(client, app_with_mock_robot):
    map_data_db.clear()
    _, robot = app_with_mock_robot
    robot.base.maps.fetch.return_value = {"compressed": "data"}

    response = client.get("/base/maps/42")
    assert response.status_code == 200
    assert response.json() == {"map_id": 42, "map_data": {"compressed": "data"}}

def test_get_compressed_map_data_cached(client, app_with_mock_robot):
    map_data_db[99] = {"cached": "yes"}
    response = client.get("/base/maps/99")
    assert response.status_code == 200
    assert response.json() == {"map_id": 99, "map_data": {"cached": "yes"}}

def test_get_compressed_map_data_not_found(client, app_with_mock_robot):
    map_data_db.clear()
    _, robot = app_with_mock_robot
    robot.base.maps.fetch.return_value = None

    response = client.get("/base/maps/77")
    assert response.status_code == 404
    assert response.json()["detail"] == "Map data not found for ID 77"

# ---------------------- POST /save-markers ----------------------

def test_save_markers_success(client):
    payload = {
        "map_id": 12,
        "markers": [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
    }
    response = client.post("/save-markers", json=payload)
    assert response.status_code == 200
    assert response.json() == payload
    assert markers_db[12] == payload["markers"]

def test_save_markers_missing_map_id(client):
    # map_id is required due to pydantic validation, so simulate invalid input
    payload = {
        "markers": [{"x": 1, "y": 2}]
    }
    response = client.post("/save-markers", json=payload)
    assert response.status_code == 422  # validation error

# ---------------------- GET /load-markers/{map_id} ----------------------

def test_load_markers_found(client):
    markers_db[55] = [{"label": "A"}, {"label": "B"}]
    response = client.get("/load-markers/55")
    assert response.status_code == 200
    assert response.json() == {"map_id": 55, "markers": [{"label": "A"}, {"label": "B"}]}

def test_load_markers_not_found(client):
    markers_db.pop(100, None)
    response = client.get("/load-markers/100")
    assert response.status_code == 200
    assert response.json() == {
        "map_id": 100,
        "markers": [],
        "warning": "No markers found for this map_id"
    }
