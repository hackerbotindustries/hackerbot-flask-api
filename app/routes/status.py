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


from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/status")
def get_status(request: Request):
    try:
        robot = request.app.state.robot
        if robot is None:
            raise HTTPException(status_code=500, detail="Robot is not initialized in app state")

        status = robot.get_current_action()
        if status is None:
            return JSONResponse(content={"status": None, "warning": "No current action available"}, status_code=204)

        return {"status": status}
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to retrieve status: {str(e)}"},
            status_code=500
        )

@router.get("/error")
def get_error(request: Request):
    try:
        robot = request.app.state.robot
        if robot is None:
            raise HTTPException(status_code=500, detail="Robot is not initialized in app state")

        error = robot.get_error()
        return {"error": error} if error else JSONResponse(
            content={"message": "No errors reported."},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to retrieve error state: {str(e)}"},
            status_code=500
        )