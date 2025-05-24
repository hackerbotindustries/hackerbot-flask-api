################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.05.19
#
# This script initializes the Flask application.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from hackerbot import Hackerbot
from app.routers import register_routes

robot = None  # Will be initialized in lifespan

@asynccontextmanager
async def lifespan(app: FastAPI):
    global robot
    print("Starting up Hackerbot...")
    robot = Hackerbot(verbose_mode=True)
    app.state.robot = robot

    yield  

    print("Cleaning up Hackerbot...")
    robot.base.destroy() 


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routes(app)

    return app