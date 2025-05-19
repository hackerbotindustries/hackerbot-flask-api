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

router = APIRouter()

# In-memory caches
map_data_db: Dict[int, dict] = {}
markers_db: Dict[int, List[dict]] = {}

# --- Request Body Schema ---
class MarkerData(BaseModel):
    map_id: int
    markers: List[dict]

# --- Routes ---

@router.post("/base/maps")
async def base_goto(request: Request, robot = Depends(get_robot)):
    """
    Navigate the robot base to a specified position on the map.

    This endpoint processes a JSON request containing the method 'goto' along with target coordinates
    and optional angle and speed parameters to command the robot base to move to the specified location.
    Example:
        {
            "method": "goto",
            "x": 1.0,
            "y": 1.0,
            "angle": 45.0,
            "speed": 1.0
        }

    Args:
        request (Request): The incoming HTTP request containing JSON data with the navigation method and parameters.

    Returns:
        dict: A dictionary with a single key "response" containing the result of the navigation command if successful.
        JSONResponse: An error response with the corresponding HTTP status code and error message if the operation fails.

    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
        HTTPException: 400 if 'method' is not 'goto' or if required parameters are missing.
    """
    try:
        data = await request.json()
        if data.get('method') == 'goto':
            x = get_required_param(data, 'x')
            y = get_required_param(data, 'y')
            angle = data.get('angle')  # Optional
            speed = data.get('speed')  # Optional

            result = robot.base.maps.goto(x, y, angle, speed)
            return {"response": result} if result else JSONResponse(
                content={"error": robot.get_error()}, status_code=500)
        else:
            raise HTTPException(status_code=422, detail="Invalid method")
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            content={"error": f"base_goto failed: {str(e)}"},
            status_code=500)

@router.get("/base/maps")
def get_map_list(request: Request, robot = Depends(get_robot)):
    """
    Get a list of available maps.

    Returns:
        JSONResponse: A dictionary with a single key "map_list" containing a list of map IDs and names.
    Raises:
        HTTPException: 404 if no map list is found.
        HTTPException: 500 if the robot is not initialized in app state or if an unknown error occurs.
    """
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
    """
    Get the current position of the robot base.

    Returns:
        JSONResponse: A dictionary with a single key "response" containing the position data.
    Raises:
        HTTPException: 500 if the robot is not initialized in app state or if there is an error retrieving the position.
    """
    try:
        result = robot.base.maps.position()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise  
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to fetch position: {str(e)}"}, status_code=500)

@router.get("/base/maps/{selected_map_id}")
def get_compressed_map_data(request: Request, selected_map_id: int, robot = Depends(get_robot)):
    """
    Retrieve compressed map data for a specific map ID.

    Args:
        request (Request): The incoming HTTP request.
        selected_map_id (int): The ID of the map to retrieve data for.

    Returns:
        dict: A dictionary containing the map ID and its associated compressed map data.

    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
        HTTPException: 404 if no map data is found for the given ID.
        JSONResponse: 500 if an unknown error occurs while fetching map data.
    """
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
