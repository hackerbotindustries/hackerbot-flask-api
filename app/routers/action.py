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


from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.dependencies import get_robot 

router = APIRouter()

@router.post("/core")
async def core_post(request: Request, robot = Depends(get_robot)):
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
async def core_version(request: Request, robot = Depends(get_robot)):
    """
    Get the version of the robot core.

    Returns a JSON response with the version number as a string if the operation is successful.
    If the robot is not initialized in app state, a 500 error is returned with the error message.
    If there is an error retrieving the version number, a 500 error is returned with the error message.

    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
    """
    try:
        result = robot.core.version()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"core_version failed: {str(e)}"}, status_code=500)

@router.post("/base")
async def base_post(request: Request, robot = Depends(get_robot)):
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
      Example: {"model_src": "en_GB-semaine-medium", "text": "Hello, world!", "speaker": None}
    - drive: Drive the robot. The JSON payload should include the linear and angular velocities.
      Example: {"linear": 0.0, "angular": 65.0}

    Returns a JSON response with a "response" key containing the result of the operation.
    If the robot is not initialized in app state, a 500 error is returned with the error message.
    If the operation is successful but the result is None, a 204 response is returned with a warning message.
    If there is an error with the operation, a 500 error is returned with the error message.

    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
    """
    try:
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
            raise HTTPException(status_code=422, detail="Invalid method")

        result = handlers[method]()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"base_post failed: {str(e)}"}, status_code=500)

@router.get("/base/status")
async def base_status(request: Request, robot = Depends(get_robot)):
    """
    Get the current status of the robot base.

    Returns:
        JSONResponse: A dictionary with a single key "response" containing the status data.
    Raises:
        HTTPException: 500 if the robot is not initialized in app state.
        JSONResponse: 500 if there is an error retrieving the status.
    """
    try:
        result = robot.base.status()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"base_status failed: {str(e)}"}, status_code=500)

@router.put("/head")
async def head_settings(request: Request, robot = Depends(get_robot)):
    """
    Set the idle mode of the robot head.

    This endpoint processes a JSON request containing the idle mode to set for the robot head.
    Example:
    {"idle-mode": "True"}

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
        data = await request.json()
        result = robot.head.set_idle_mode(data.get('idle-mode'))
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"head_settings failed: {str(e)}"}, status_code=500)

@router.post("/head")
async def head_command(request: Request, robot = Depends(get_robot)):
    """
    Execute commands for controlling the robot's head.

    This endpoint processes a JSON request containing the method to execute, along with any required parameters
    for controlling the robot's head, such as 'look' or 'gaze'.
    Example:
        {
            "method": "look",
            "yaw": 180,
            "pitch": 180,
            "speed": 40
        }
        {
            "method": "gaze",
            "x": 1.0,
            "y": 1.0
        }

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
        data = await request.json()
        method = data.get('method')

        if method == 'look':
            yaw = data.get('yaw')
            pitch = data.get('pitch')
            speed = data.get('speed')
            if yaw is None or pitch is None or speed is None:
                raise HTTPException(status_code=400, detail="Missing 'yaw', 'pitch', or 'speed'")
            result = robot.head.look(yaw, pitch, speed)

        elif method == 'gaze':
            x = data.get('x')
            y = data.get('y')
            if x is None or y is None:
                raise HTTPException(status_code=400, detail="Missing 'x' or 'y'")
            result = robot.head.eyes.gaze(x, y)
        else:
            raise HTTPException(status_code=422, detail="Invalid method")

        return {"response": result} if result else JSONResponse(
            content={"error": robot.get_error()}, status_code=500
        )
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"head_command failed: {str(e)}"}, status_code=500)

@router.post("/arm/gripper")
async def gripper_command(request: Request, robot = Depends(get_robot)):
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
        data = await request.json()
        method = data.get('method')

        if method == 'calibrate':
            result = robot.arm.gripper.calibrate()
        elif method == 'open':
            result = robot.arm.gripper.open()
        elif method == 'close':
            result = robot.arm.gripper.close()
        else:
            raise HTTPException(status_code=422, detail="Invalid method")

        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"gripper_command failed: {str(e)}"}, status_code=500)

@router.post("/arm")
async def arm_command(request: Request, robot = Depends(get_robot)):
    """
    Execute commands for controlling the arm of the robot.

    This endpoint processes a JSON request containing the method to execute, along with any required parameters
    for controlling the arm, such as 'move-joint' or 'move-joints'. Parameters may include 'joint', 'angle', and 'speed'.
    Example: 
    {"method": "move-joint", "joint": 1, "angle": 45.0, "speed": 1.0}, 
    {"method": "move-joints", "angles": [45.0, 0.0, 0.0, 0.0, 0.0, 0.0], "speed": 1.0}

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
        data = await request.json()
        method = data.get('method')

        if method == 'move-joint':
            joint = data.get('joint')
            angle = data.get('angle')
            speed = data.get('speed')
            if joint is None or angle is None or speed is None:
                raise HTTPException(status_code=400, detail="Missing 'joint', 'angle', or 'speed'")
            result = robot.arm.move_joint(joint, angle, speed)

        elif method == 'move-joints':
            angles = data.get('angles')
            speed = data.get('speed')
            if angles is None or not isinstance(angles, list) or speed is None:
                raise HTTPException(status_code=400, detail="Missing or invalid 'angles' or 'speed'")
            result = robot.arm.move_joints(angles, speed)

        else:
            raise HTTPException(status_code=422, detail="Invalid method")

        return {"response": result} if result else JSONResponse(
            content={"error": robot.get_error()}, status_code=500
        )
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": f"arm_command failed: {str(e)}"}, status_code=500)