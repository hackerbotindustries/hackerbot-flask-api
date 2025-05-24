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
    try:
        result = robot.head.set_idle_mode(cmd.idle_mode)
        return {"response": result} if result else JSONResponse(
            content={"error": robot.get_error()}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"head_settings failed: {str(e)}"}, status_code=500)

@router.post("/head")
async def head_command(cmd: HeadCommand, robot = Depends(get_robot)):
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
