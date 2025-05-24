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
# This script contains the arm Fast API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Literal, Optional, Union
from app.dependencies import get_robot

# --- MODELS: ARM ---
class MoveJointCommand(BaseModel):
    method: Literal["move-joint"]
    joint: int
    angle: float
    speed: float

class MoveJointsCommand(BaseModel):
    method: Literal["move-joints"]
    angles: list[float]
    speed: float

ArmCommand = Union[MoveJointCommand, MoveJointsCommand]

class GripperCalibrateCommand(BaseModel):
    method: Literal["calibrate"]

class GripperOpenCommand(BaseModel):
    method: Literal["open"]

class GripperCloseCommand(BaseModel):
    method: Literal["close"]

GripperCommand = Union[
    GripperCalibrateCommand,
    GripperOpenCommand,
    GripperCloseCommand
]

@router.post("/arm")
async def arm_command(cmd: ArmCommand, robot = Depends(get_robot)):
    """
    Handles POST requests to /arm.

    This endpoint is used to send commands to the arm.

    The request body should contain a JSON object with a "method" key and
    optionally other keys depending on the method. The following methods are
    supported:

    - "move-joint": Move the specified joint to the specified angle.
      The request body should contain the following keys:

      - "joint": The joint to move.
      - "angle": The angle to move to in degrees.
      - "speed": The speed at which to move the joint.
    - "move-joints": Move the arm to the specified angles.
      The request body should contain the following keys:

      - "angles": A list of angles to move to in degrees.
      - "speed": The speed at which to move the arm.

    If the request body is invalid or the method is not recognized, a 422 error
    is returned.

    If the request is successful, a JSON response is returned with a "response"
    key containing the result of the command. If there is an error, a JSON
    response is returned with an "error" key containing the error message and
    a 500 status code is returned.
    """
    try:
        if isinstance(cmd, MoveJointCommand):
            result = robot.arm.move_joint(cmd.joint, cmd.angle, cmd.speed)
        elif isinstance(cmd, MoveJointsCommand):
            result = robot.arm.move_joints(cmd.angles, cmd.speed)
        else:
            raise HTTPException(status_code=422, detail="Invalid method")

        return {"response": result} if result else JSONResponse(
            content={"error": robot.get_error()}, status_code=500)

    except Exception as e:
        return JSONResponse(content={"error": f"arm_command failed: {str(e)}"}, status_code=500)

@router.post("/arm/gripper")
async def gripper_command(cmd: GripperCommand, robot = Depends(get_robot)):
    """
    Handles POST requests to /arm/gripper.

    This endpoint is used to send commands to the gripper.

    The request body should contain a JSON object with a "method" key and
    optionally other keys depending on the method. The following methods are
    supported:

    - "calibrate": Calibrate the gripper.
    - "open": Open the gripper.
    - "close": Close the gripper.

    If the request body is invalid or the method is not recognized, a 422 error
    is returned.

    If the request is successful, a JSON response is returned with a "response"
    key containing the result of the command. If there is an error, a JSON
    response is returned with an "error" key containing the error message and
    a 500 status code is returned.
    """
    try:
        if isinstance(cmd, GripperCalibrateCommand):
            result = robot.arm.gripper.calibrate()
        elif isinstance(cmd, GripperOpenCommand):
            result = robot.arm.gripper.open()
        elif isinstance(cmd, GripperCloseCommand):
            result = robot.arm.gripper.close()
        else:
            raise HTTPException(status_code=422, detail="Invalid method")

        return {"response": result} if result else JSONResponse(
            content={"error": robot.get_error()}, status_code=500)

    except Exception as e:
        return JSONResponse(content={"error": f"gripper_command failed: {str(e)}"}, status_code=500)