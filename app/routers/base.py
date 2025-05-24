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
# This script contains the base Fast API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.dependencies import get_robot
from app.models.base import BaseCommand, InitializeRequest, ModeRequest, StartRequest, QuickmapRequest, DockRequest, KillRequest, TriggerBumpRequest, SpeakRequest, DriveRequest

router = APIRouter()

@router.post("/base")
async def base_post(cmd: BaseCommand, robot = Depends(get_robot)):
    """
    Handles POST requests to /base endpoint.

    This function processes various base commands by determining the type of request
    and invoking the appropriate method on the robot's base. The supported commands are:

    - "initialize": Initializes the robot's base.
    - "mode": Sets the mode of the robot's base using the provided mode_id.
    - "start": Starts the robot's base operations.
    - "quickmap": Performs a quick mapping operation with the robot's base.
    - "dock": Docks the robot to its station.
    - "kill": Stops all operations of the robot's base.
    - "trigger-bump": Triggers a bump using the specified left and right parameters.
    - "speak": Makes the robot speak the provided text using the specified model and speaker_id.
      Ex: {"model_src": "en_GB-semaine-medium", "text": "Hello, world!", "speaker_id": null}
    - "drive": Drives the robot with the specified linear and angular velocities.
      Ex: {"linear_velocity": 0.0, "angle_velocity": 65}

    Returns a JSON response containing the result of the command under the "response" key if successful.
    If an error occurs, returns a JSON response with an "error" key containing the error message.
    Raises a 422 HTTPException if the command method is invalid.
    """
    try:
        if isinstance(cmd, InitializeRequest):
            result = robot.base.initialize()
        elif isinstance(cmd, ModeRequest):
            result = robot.base.set_mode(cmd.mode_id)
        elif isinstance(cmd, StartRequest):
            result = robot.base.start()
        elif isinstance(cmd, QuickmapRequest):
            result = robot.base.quickmap()
        elif isinstance(cmd, DockRequest):
            result = robot.base.dock()
        elif isinstance(cmd, KillRequest):
            result = robot.base.kill()
        elif isinstance(cmd, TriggerBumpRequest):
            result = robot.base.trigger_bump(cmd.left, cmd.right)
        elif isinstance(cmd, SpeakRequest):
            result = robot.base.speak(cmd.model_src, cmd.text, cmd.speaker_id)
        elif isinstance(cmd, DriveRequest):
            result = robot.base.drive(cmd.linear_velocity, cmd.angle_velocity)
        else:
            raise HTTPException(status_code=422, detail="Invalid method")

        return {"response": result} if result else JSONResponse(
            content={"error": robot.get_error()}, status_code=500)

    except Exception as e:
        return JSONResponse(
            content={"error": f"base_post failed: {str(e)}"},
            status_code=500)
