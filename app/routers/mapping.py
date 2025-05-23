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


from fastapi import APIRouter, Request, HTTPException, Depends
from app.utils.request_helpers import get_required_param
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.dependencies import get_robot
from typing import Literal, Optional

router = APIRouter()

# In-memory caches
map_data_db: Dict[int, dict] = {}
markers_db: Dict[int, List[dict]] = {}

# --- Request Body Schema ---
class MarkerData(BaseModel):
    map_id: int
    markers: List[dict]

# --- Routes ---
class GotoRequest(BaseModel):
    method: Literal["goto"]
    x: float
    y: float
    angle: Optional[float] = None
    speed: Optional[float] = None

@router.post("/base/maps")
async def base_goto(cmd: GotoRequest, robot = Depends(get_robot)):
    try:
        result = robot.base.maps.goto(cmd.x, cmd.y, cmd.angle, cmd.speed)
        if result:
            return {"response": result}
        else:
            return JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except Exception as e:
        return JSONResponse(
            content={"error": f"base_goto failed: {str(e)}"},
            status_code=500)

@router.get("/base/maps")
def get_map_list(request: Request, robot = Depends(get_robot)):
    try:
        map_list = robot.base.maps.list()
        if map_list is None:
            raise HTTPException(status_code=404, detail="No map list found")
        return {"map_list": map_list}
    except HTTPException:
        raise  
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to fetch map list: {str(e)}"}, status_code=500)

@router.get("/base/maps/position")
async def base_position(request: Request, robot = Depends(get_robot)):  
    try:
        result = robot.base.maps.position()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise  
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to fetch position: {str(e)}"}, status_code=500)

@router.get("/base/maps/{selected_map_id}")
def get_compressed_map_data(request: Request, selected_map_id: int, robot = Depends(get_robot)):
    try:
        if selected_map_id not in map_data_db:
            map_data = robot.base.maps.fetch(selected_map_id)
            if map_data is None:
                raise HTTPException(status_code=404, detail=f"Map data not found for ID {selected_map_id}")
            map_data_db[selected_map_id] = map_data

        return {
            "map_id": selected_map_id,
            "map_data": map_data_db[selected_map_id]
        }
    except HTTPException:
        raise  
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to fetch map data: {str(e)}"}, status_code=500)

@router.post("/save-markers")
def save_markers(data: MarkerData):
    """
    Save the given markers to the database.

    Args:
        data (MarkerData): A pydantic model containing the map ID and a list of markers to save.

    Returns:
        dict: A diction"ary containing the map ID and the saved markers.

    Raises:
        HTTPException: 400 if the map ID is missing or invalid.
        HTTPException: 500 if there is an error saving the markers.
    """
    try:
        map_id = get_required_param(data.__dict__, 'map_id')
        markers_db[data.map_id] = data.markers
        return {
            "map_id": data.map_id,
            "markers": data.markers
        }
    except HTTPException:
        raise  
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to save markers: {str(e)}"}, status_code=500)

@router.get("/load-markers/{map_id}")
def load_markers(map_id: int):
    """
    Load the markers associated with a given map ID.

    Args:
        map_id (int): The ID of the map to load markers from.

    Returns:
        dict: A dictionary containing the map ID and a list of markers associated with the map ID.

    Raises:
        HTTPException: 400 if the map ID is invalid or missing.
        HTTPException: 500 if there is an error loading the markers.
    """
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
    except HTTPException:
        raise  
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to load markers: {str(e)}"}, status_code=500)