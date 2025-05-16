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
    try:
        robot = request.app.state.robot
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
            raise HTTPException(status_code=400, detail="Invalid method")

        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"core_post failed: {str(e)}"}, status_code=500)

@router.get("/core/version")
async def core_version(request: Request):
    try:
        robot = request.app.state.robot
        result = robot.core.version()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"core_version failed: {str(e)}"}, status_code=500)

@router.post("/base")
async def base_post(request: Request):
    try:
        robot = request.app.state.robot
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
    except Exception as e:
        return JSONResponse(content={"error": f"base_post failed: {str(e)}"}, status_code=500)


@router.get("/base/status")
async def base_status(request: Request):
    try:
        robot = request.app.state.robot
        result = robot.base.status()
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"base_status failed: {str(e)}"}, status_code=500)

@router.post("/base/maps")
async def base_goto(request: Request):
    try:
        robot = request.app.state.robot
        data = await request.json()
        if data.get('method') == 'goto':
            if data.get('x') is None or data.get('y') is None:
                raise HTTPException(status_code=400, detail="Missing parameters")
            result = robot.base.maps.goto(data.get('x'), data.get('y'), data.get('angle'), data.get('speed'))
            return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
        else:
            raise HTTPException(status_code=400, detail="Invalid method")
    except Exception as e:
        return JSONResponse(content={"error": f"base_goto failed: {str(e)}"}, status_code=500)

@router.put("/head")
async def head_settings(request: Request):
    try:
        robot = request.app.state.robot
        data = await request.json()
        result = robot.head.set_idle_mode(data.get('idle-mode'))
        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"head_settings failed: {str(e)}"}, status_code=500)

@router.post("/head")
async def head_command(request: Request):
    try:
        robot = request.app.state.robot
        data = await request.json()
        method = data.get('method')

        if method == 'look':
            result = robot.head.look(data.get('yaw'), data.get('pitch'), data.get('speed'))
        elif method == 'gaze':
            result = robot.head.eyes.gaze(data.get('x'), data.get('y'))
        else:
            raise HTTPException(status_code=400, detail="Invalid method")

        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"head_command failed: {str(e)}"}, status_code=500)

@router.post("/arm/gripper")
async def gripper_command(request: Request):
    try:
        robot = request.app.state.robot
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
    except Exception as e:
        return JSONResponse(content={"error": f"gripper_command failed: {str(e)}"}, status_code=500)

@router.post("/arm")
async def arm_command(request: Request):
    try:
        robot = request.app.state.robot
        data = await request.json()
        method = data.get('method')

        if method == 'move-joint':
            result = robot.arm.move_joint(data.get('joint'), data.get('angle'), data.get('speed'))
        elif method == 'move-joints':
            result = robot.arm.move_joints(data.get('angles'), data.get('speed'))
        else:
            raise HTTPException(status_code=400, detail="Invalid method")

        return {"response": result} if result else JSONResponse(content={"error": robot.get_error()}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": f"arm_command failed: {str(e)}"}, status_code=500)