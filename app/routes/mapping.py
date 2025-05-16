################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.05.16
#
# This script contains the mapping API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
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

@router.get("/base/maps")
def get_map_list(request: Request):
    try:
        robot = request.app.state.robot
        if not robot:
            raise HTTPException(status_code=500, detail="Robot not configured")

        map_list = robot.base.maps.list()
        if map_list is None:
            raise HTTPException(status_code=404, detail="No map list found")
        return {"map_list": map_list}
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to fetch map list: {str(e)}"}, status_code=500)

@router.get("/base/maps/position")
async def base_position(request: Request):  
    try:
        robot = request.app.state.robot
        if not robot:
            raise HTTPException(status_code=500, detail="Robot not configured")

        result = robot.base.maps.position()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to fetch position: {str(e)}"}, status_code=500)

@router.get("/base/maps/{selected_map_id}")
def get_compressed_map_data(request: Request, selected_map_id: int):
    try:
        robot = request.app.state.robot
        if not robot:
            raise HTTPException(status_code=500, detail="Robot not configured")

        if selected_map_id not in map_data_db:
            map_data = robot.base.maps.fetch(selected_map_id)
            if map_data is None:
                raise HTTPException(status_code=404, detail=f"Map data not found for ID {selected_map_id}")
            map_data_db[selected_map_id] = map_data

        return {
            "map_id": selected_map_id,
            "map_data": map_data_db[selected_map_id]
        }
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to fetch map data: {str(e)}"}, status_code=500)

@router.post("/save-markers")
def save_markers(data: MarkerData):
    try:
        if data.map_id is None:
            raise HTTPException(status_code=400, detail="map_id is required")

        markers_db[data.map_id] = data.markers
        return {
            "map_id": data.map_id,
            "markers": data.markers
        }
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to save markers: {str(e)}"}, status_code=500)

@router.get("/load-markers/{map_id}")
def load_markers(map_id: int):
    try:
        markers = markers_db.get(map_id)
        if markers is None:
            return JSONResponse(
                content={"map_id": map_id, "markers": [], "warning": "No markers found for this map_id"},
                status_code=200
            )
        return {
            "map_id": map_id,
            "markers": markers
        }
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to load markers: {str(e)}"}, status_code=500)
