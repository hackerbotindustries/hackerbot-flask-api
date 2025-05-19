################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.01
#
# This script contains the dependencies for the FAST API application.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from fastapi import Request, HTTPException

def get_robot(request: Request):
    robot = getattr(request.app.state, "robot", None)
    if robot is None:
        raise HTTPException(status_code=500, detail="Robot is not initialized in app state")
    return robot