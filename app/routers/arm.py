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