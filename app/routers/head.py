################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.05.23
#
# This script contains the head Fast API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Literal, Optional, Union
from app.dependencies import get_robot

router = APIRouter()

# --- MODELS ---
class LookCommand(BaseModel):
    method: Literal["look"]
    pan: float
    tilt: float
    speed: float

class GazeCommand(BaseModel):
    method: Literal["gaze"]
    x: float
    y: float

HeadCommand = Union[LookCommand, GazeCommand]

class IdleModeSettings(BaseModel):
    idle_mode: bool

# --- ENDPOINTS ---
@router.put("/head")
async def head_settings(cmd: IdleModeSettings, robot = Depends(get_robot)):
    """
    Handles PUT requests to /head for setting idle mode.

    This endpoint is used to set the idle mode of the robot's head. The request
    body should contain a JSON object with an "idle_mode" key indicating whether
    the idle mode should be enabled or disabled.

    - "idle_mode": A boolean indicating the desired state of the idle mode.

    If the request is successful, a JSON response is returned with a "response"
    key containing the result of the operation. If there is an error, a JSON
    response is returned with an "error" key containing the error message and
    a 500 status code is returned.
    """
    try:
        result = robot.head.set_idle_mode(cmd.idle_mode)
        return {"response": result} if result else JSONResponse(
            content={"error": robot.get_error()}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"head_settings failed: {str(e)}"}, status_code=500)

@router.post("/head")
async def head_command(cmd: HeadCommand, robot = Depends(get_robot)):
    """
    Handles POST requests to /head.

    This endpoint is used to send commands to the robot's head.

    The request body should contain a JSON object with a "method" key and
    optionally other keys depending on the method. The following methods are
    supported:

    - "look": Moves the robot's head to the specified pan and tilt angles.
      The request body should contain the following keys:

      - "pan": The pan angle to move to in degrees.
      - "tilt": The tilt angle to move to in degrees.
      - "speed": The speed at which to move the head.
    - "gaze": Moves the robot's eyes to the specified x and y coordinates.
      The request body should contain the following keys:

      - "x": The x coordinate to move to.
      - "y": The y coordinate to move to.

    If the request body is invalid or the method is not recognized, a 422 error
    is returned.

    If the request is successful, a JSON response is returned with a "response"
    key containing the result of the command. If there is an error, a JSON
    response is returned with an "error" key containing the error message and
    a 500 status code is returned.
    """
    try:
        if isinstance(cmd, LookCommand):
            result = robot.head.look(cmd.pan, cmd.tilt, cmd.speed)
        elif isinstance(cmd, GazeCommand):
            result = robot.head.eyes.gaze(cmd.x, cmd.y)
        else:
            raise HTTPException(status_code=422, detail="Invalid method")

        return {"response": result} if result else JSONResponse(
            content={"error": robot.get_error()}, status_code=500)

    except Exception as e:
        return JSONResponse(
            content={"error": f"head_command failed: {str(e)}"},
            status_code=500
        )
