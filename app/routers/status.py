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
# This script contains the status API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.dependencies import get_robot

router = APIRouter()

@router.get("/status")
def get_status(request: Request, robot = Depends(get_robot)):
    """
    Get the current status of the robot.

    Returns a JSON response with a "status" key, which is None if no current action is available.
    If no current action is available, a 204 status code is returned and a warning is included in the response.

    Raises a 500 error if there is a problem retrieving the status.
    """
    try:
        status = robot.get_current_action()
        if status is None:
            return JSONResponse(content={"status": None, "warning": "No current action available"}, status_code=204)

        return {"status": status}
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to retrieve status: {str(e)}"},
            status_code=500
        )

@router.get("/error")
def get_error(request: Request, robot = Depends(get_robot)):
    """
    Get the current error state of the robot.

    Returns a JSON response with an "error" key, which is None if no error state is available.
    If no error state is available, a 200 status code is returned with a message "None".
    If the error state is available, a 200 status code is returned with the error message.

    Raises a 500 error if there is a problem retrieving the error state.
    """
    try:
        error = robot.get_error()
        return {"error": error} if error else JSONResponse(
            content={"message": "None"},
            status_code=200
        )
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to retrieve error state: {str(e)}"},
            status_code=500
        )