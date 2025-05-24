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
# This script registers the routes for the Flask application.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from app.routers import status, mapping, core, base, head, arm

def register_routes(app):
    # v1 routes
    app.include_router(status.router, prefix="/api/v1", tags=["status"])
    app.include_router(mapping.router, prefix="/api/v1", tags=["mapping"])
    app.include_router(core.router, prefix="/api/v1", tags=["core"])
    app.include_router(base.router, prefix="/api/v1", tags=["base"])
    app.include_router(head.router, prefix="/api/v1", tags=["head"])
    app.include_router(arm.router, prefix="/api/v1", tags=["arm"])
    
    # v2 routes
    # app.include_router(status.router, prefix="/api/v2", tags=["status"])
    # app.include_router(mapping.router, prefix="/api/v2", tags=["mapping"])
    # app.include_router(core.router, prefix="/api/v2", tags=["core"])
    # app.include_router(base.router, prefix="/api/v2", tags=["base"])