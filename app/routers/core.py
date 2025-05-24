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
# This script contains the core Fast API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from pydantic import BaseModel
from typing import Optional, Union, Literal
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from app.dependencies import get_robot

class PingRequest(BaseModel):
    method: Literal["ping"]

class SettingsRequest(BaseModel):
    method: Literal["settings"]
    json_responses: Optional[bool] = None
    tofs_enabled: Optional[bool] = None

CoreCommand = Union[PingRequest, SettingsRequest]

router = APIRouter()

@router.post("/core")
async def core_post(cmd: CoreCommand, robot = Depends(get_robot)):
    """
    Handles POST requests to /core.

    This endpoint is used to send commands to the core of the robot.

    The request body should contain a JSON object with a "method" key and
    optionally other keys depending on the method. The following methods are
    supported:

    - "ping": A no-op request that returns "pong" if the robot is online.
    - "settings": A request to change the settings of the robot. The following
      settings can be changed:

      - "json_responses": Whether the robot should return JSON responses.
      - "tofs_enabled": Whether the TOFs should be enabled.

    If the request body is invalid or the method is not recognized, a 422 error
    is returned.

    If the request is successful, a JSON response is returned with a "response"
    key containing the result of the command. If there is an error, a JSON
    response is returned with an "error" key containing the error message and
    a 500 status code is returned.
    """
    try:
        if isinstance(cmd, PingRequest):
            result = robot.core.ping()
        elif isinstance(cmd, SettingsRequest):
            if cmd.json_responses is not None:
                result = robot.set_json_mode(cmd.json_responses)
            if cmd.tofs_enabled is not None:
                result = robot.set_TOFs(cmd.tofs_enabled)

            if not result:
                raise HTTPException(status_code=422, detail="Missing settings fields")
        else:
            raise HTTPException(status_code=422, detail="Invalid method")

        return {"response": result} if result else JSONResponse(
            content={"error": robot.get_error()}, status_code=500)

    except Exception as e:
        return JSONResponse(
            content={"error": f"core_post failed: {str(e)}"},
            status_code=500)

@router.get("/core/version")
async def core_version(request: Request, robot = Depends(get_robot)):
    """
    Get the current version of the robot's core system.

    This endpoint returns a JSON response with a "response" key containing
    the version information of the robot's core system. If the version
    information is not available, a 500 status code is returned with an
    error message.

    Raises a 500 error if there is a problem retrieving the version.
    """
    try:
        result = robot.core.version()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"core_version failed: {str(e)}"}, status_code=500)