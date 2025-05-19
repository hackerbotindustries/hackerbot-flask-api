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
# This script contains the action Fast API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/core")
async def core_post(request: Request):
    """
    Handle POST requests to the /core endpoint.

    This function processes incoming requests to perform core operations on the robot.
    It supports the following methods:
    - 'ping': Checks the connectivity with the robot core.
    - 'settings': Configures robot settings, including enabling/disabling JSON responses
      and time-of-flight sensors.

    Args:
        request (Request): The incoming HTTP request containing JSON data with the method
        and any additional parameters required.

    Returns:
        dict: A dictionary with a single key "response" containing the result of the operation
        if successful.
        JSONResponse: An error response with the corresponding HTTP status code and error message
        if the operation fails or if an error occurs.

    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
        HTTPException: 400 if 'method' is missing in the request or if required parameters are missing.
        HTTPException: 422 if the method provided is invalid.
    """
    try:
        robot = getattr(request.app.state, "robot", None)
        if robot is None:
            raise HTTPException(status_code=500, detail="Robot is not initialized in app state")
        data = await request.json()
        if 'method' not in data:
            raise HTTPException(status_code=400, detail="Missing method")

        if data['method'] == 'ping':
            result = robot.core.ping()
        elif data['method'] == 'settings':
            result = True
            if 'json-responses' in data:
                result &= robot.set_json_mode(data['json-responses'])
            if 'tofs-enabled' in data:
                result &= robot.set_TOFs(data['tofs-enabled'])
        else:
            raise HTTPException(status_code=422, detail="Invalid method")

        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"core_post failed: {str(e)}"}, status_code=500)

@router.get("/core/version")
async def core_version(request: Request):
    """
    Get the version of the robot core.

    Returns a JSON response with the version number as a string if the operation is successful.
    If the robot is not initialized in app state, a 500 error is returned with the error message.
    If there is an error retrieving the version number, a 500 error is returned with the error message.

    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
    """
    try:
        robot = getattr(request.app.state, "robot", None)
        if robot is None:
            raise HTTPException(status_code=500, detail="Robot is not initialized in app state")
        result = robot.core.version()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"core_version failed: {str(e)}"}, status_code=500)

@router.post("/base")
async def base_post(request: Request):
    """
    Perform a base command.

    Accepts a JSON payload containing the command to run. The accepted commands are:

    - initialize: Initialize the robot base.
    - mode: Set the mode of the robot base. The JSON payload should include the mode ID.
    - start: Start the robot base.
    - quickmap: Start the quickmap process.
    - dock: Dock the robot.
    - kill: Kill the robot base.
    - trigger-bump: Trigger the bump sensors. The JSON payload should include the left and right trigger states.
    - speak: Speak a phrase. The JSON payload should include the model source, text, and speaker ID.
    - drive: Drive the robot. The JSON payload should include the linear and angular velocities.

    Returns a JSON response with a "response" key containing the result of the operation.
    If the robot is not initialized in app state, a 500 error is returned with the error message.
    If the operation is successful but the result is None, a 204 response is returned with a warning message.
    If there is an error with the operation, a 500 error is returned with the error message.

    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
    """
    try:
        robot = getattr(request.app.state, "robot", None)
        if robot is None:
            raise HTTPException(status_code=500, detail="Robot is not initialized in app state")
        data = await request.json()
        method = data.get('method')
        if not method:
            raise HTTPException(status_code=400, detail="Missing method")

        handlers = {
            'initialize': robot.base.initialize,
            'mode': lambda: robot.base.set_mode(data.get('mode_id')),
            'start': robot.base.start,
            'quickmap': robot.base.quickmap,
            'dock': robot.base.dock,
            'kill': robot.base.kill,
            'trigger-bump': lambda: robot.base.trigger_bump(data.get('left'), data.get('right')),
            'speak': lambda: robot.base.speak(data.get('model_src'), data.get('text'), data.get("speaker_id")),
            'drive': lambda: robot.base.drive(data.get('linear_velocity'), data.get('angle_velocity'))
        }

        if method not in handlers:
            raise HTTPException(status_code=400, detail="Invalid method")

        result = handlers[method]()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"base_post failed: {str(e)}"}, status_code=500)


@router.get("/base/status")
async def base_status(request: Request):
    """
    Get the current status of the robot base.

    Returns:
        JSONResponse: A dictionary with a single key "response" containing the status data.
    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
        JSONResponse: 500 if there is an error retrieving the status.
    """
    try:
        robot = getattr(request.app.state, "robot", None)
        if robot is None:
            raise HTTPException(status_code=500, detail="Robot is not initialized in app state")
        result = robot.base.status()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"base_status failed: {str(e)}"}, status_code=500)

@router.post("/base/maps")
async def base_goto(request: Request):
    """
    Navigate the robot base to a specified position on the map.

    This endpoint processes a JSON request containing the method 'goto' along with target coordinates
    and optional angle and speed parameters to command the robot base to move to the specified location.

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
        robot = getattr(request.app.state, "robot", None)
        if robot is None:
            raise HTTPException(status_code=500, detail="Robot is not initialized in app state")
        data = await request.json()
        if data.get('method') == 'goto':
            if data.get('x') is None or data.get('y') is None:
                raise HTTPException(status_code=400, detail="Missing parameters")
            result = robot.base.maps.goto(data.get('x'), data.get('y'), data.get('angle'), data.get('speed'))
            return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
        else:
            raise HTTPException(status_code=400, detail="Invalid method")
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"base_goto failed: {str(e)}"}, status_code=500)

@router.put("/head")
async def head_settings(request: Request):
    """
    Set the idle mode of the robot head.

    This endpoint processes a JSON request containing the idle mode to set for the robot head.
    The accepted idle modes are 'idle', 'relaxed', 'focused', and 'sleeping'.

    Args:
        request (Request): The incoming HTTP request containing JSON data with the idle mode to set.

    Returns:
        dict: A dictionary with a single key "response" containing the result of the operation if successful.
        JSONResponse: An error response with the corresponding HTTP status code and error message if the operation fails.

    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
        HTTPException: 400 if 'idle-mode' is not set or is invalid.
    """
    try:
        robot = getattr(request.app.state, "robot", None)
        if robot is None:
            raise HTTPException(status_code=500, detail="Robot is not initialized in app state")
        data = await request.json()
        result = robot.head.set_idle_mode(data.get('idle-mode'))
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"head_settings failed: {str(e)}"}, status_code=500)

@router.post("/head")
async def head_command(request: Request):
    """
    Execute commands for controlling the robot's head.

    This endpoint processes a JSON request containing the method to execute, along with any required parameters
    for controlling the robot's head, such as 'look' or 'gaze'.

    Args:
        request (Request): The incoming HTTP request containing JSON data with the command method and parameters.

    Returns:
        dict: A dictionary with a single key "response" containing the result of the command if successful.
        JSONResponse: An error response with the corresponding HTTP status code and error message if the operation fails.

    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
        HTTPException: 400 if the method is invalid or missing required parameters.
    """
    try:
        robot = getattr(request.app.state, "robot", None)
        if robot is None:
            raise HTTPException(status_code=500, detail="Robot is not initialized in app state")
        data = await request.json()
        method = data.get('method')

        if method == 'look':
            result = robot.head.look(data.get('yaw'), data.get('pitch'), data.get('speed'))
        elif method == 'gaze':
            result = robot.head.eyes.gaze(data.get('x'), data.get('y'))
        else:
            raise HTTPException(status_code=400, detail="Invalid method")

        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"head_command failed: {str(e)}"}, status_code=500)

@router.post("/arm/gripper")
async def gripper_command(request: Request):
    """
    Execute commands for controlling the gripper of the robot's arm.

    This endpoint processes a JSON request containing the method to execute, along with any required parameters
    for controlling the gripper, such as 'calibrate', 'open', or 'close'.

    Args:
        request (Request): The incoming HTTP request containing JSON data with the command method and parameters.

    Returns:
        dict: A dictionary with a single key "response" containing the result of the command if successful.
        JSONResponse: An error response with the corresponding HTTP status code and error message if the operation fails.

    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
        HTTPException: 400 if the method is invalid or missing required parameters.
    """
    try:
        robot = getattr(request.app.state, "robot", None)
        if robot is None:
            raise HTTPException(status_code=500, detail="Robot is not initialized in app state")
        data = await request.json()
        method = data.get('method')

        if method == 'calibrate':
            result = robot.arm.gripper.calibrate()
        elif method == 'open':
            result = robot.arm.gripper.open()
        elif method == 'close':
            result = robot.arm.gripper.close()
        else:
            raise HTTPException(status_code=400, detail="Invalid method")

        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"gripper_command failed: {str(e)}"}, status_code=500)

@router.post("/arm")
async def arm_command(request: Request):
    """
    Execute commands for controlling the arm of the robot.

    This endpoint processes a JSON request containing the method to execute, along with any required parameters
    for controlling the arm, such as 'move-joint' or 'move-joints'.

    Args:
        request (Request): The incoming HTTP request containing JSON data with the command method and parameters.

    Returns:
        dict: A dictionary with a single key "response" containing the result of the command if successful.
        JSONResponse: An error response with the corresponding HTTP status code and error message if the operation fails.

    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
        HTTPException: 400 if the method is invalid or missing required parameters.
    """
    try:
        robot = getattr(request.app.state, "robot", None)
        if robot is None:
            raise HTTPException(status_code=500, detail="Robot is not initialized in app state")
        data = await request.json()
        method = data.get('method')

        if method == 'move-joint':
            result = robot.arm.move_joint(data.get('joint'), data.get('angle'), data.get('speed'))
        elif method == 'move-joints':
            result = robot.arm.move_joints(data.get('angles'), data.get('speed'))
        else:
            raise HTTPException(status_code=400, detail="Invalid method")

        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"arm_command failed: {str(e)}"}, status_code=500)