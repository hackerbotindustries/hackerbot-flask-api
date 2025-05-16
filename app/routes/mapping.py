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
# This script contains the mapping API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

router = APIRouter()

# In-memory caches
map_data_db: Dict[int, dict] = {}
markers_db: Dict[int, List[dict]] = {}

# --- Request Body Schema ---
class MarkerData(BaseModel):
    map_id: int
    markers: List[dict]

# --- Routes ---

@router.get("/api/v1/base/maps")
def get_map_list(request: Request):
    robot = request.app.state.robot
    map_list = robot.base.maps.list()
    if map_list is None:
        raise HTTPException(status_code=404, detail="No map list found")
    return {"map_list": map_list}

@router.get("/api/v1/base/maps/{selected_map_id}")
def get_compressed_map_data(request: Request, selected_map_id: int):
    if selected_map_id not in map_data_db:
        robot = request.app.state.robot
        if not robot:
            raise HTTPException(status_code=500, detail="Robot not configured")
        map_data = robot.base.maps.fetch(selected_map_id)
        if map_data is None:
            raise HTTPException(status_code=404, detail=f"Map data not found: {selected_map_id}")
        map_data_db[selected_map_id] = map_data

    return {
        "map_id": selected_map_id,
        "map_data": map_data_db[selected_map_id]
    }

@router.post("/api/save-markers")
def save_markers(data: MarkerData):
    if data.map_id is None:
        raise HTTPException(status_code=400, detail="map_id is required")

    markers_db[data.map_id] = data.markers
    return {
        "map_id": data.map_id,
        "markers": data.markers
    }

@router.get("/api/load-markers/{map_id}")
def load_markers(map_id: int):
    markers = markers_db.get(map_id, [])
    return {
        "map_id": map_id,
        "markers": markers
    }
