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
# This script initializes the Flask application.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from flask import Flask, g
from flask_cors import CORS
from app.routes import register_routes
from hackerbot import Hackerbot

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('app.config.Config')

    # Create a single controller instance
    robot = Hackerbot()
    robot.base.initialize()
    
    # Store everything in app.config
    app.config['ROBOT'] = robot

    # Enable CORS (Allows frontend to communicate with backend)
    CORS(app)

    # Register all routes
    register_routes(app)

    return app
