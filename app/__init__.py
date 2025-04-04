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


#test change
from flask import Flask, g
from flask_cors import CORS
from app.routes import register_routes
import hackerbot_helper as hhp

def create_app():
    app = Flask(__name__)

    # app.before_request(connect_robot)

    # Load configuration
    app.config.from_object('app.config.Config')

    # Create a single controller instance
    robot = hhp.ProgrammedController()
    robot.init_driver()
    robot.activate_machine_mode()
    
    # Store everything in app.config
    app.config['ROBOT'] = robot
    app.config['MAP_LIST'] = robot.get_map_list()
    app.config['MAP_DATA'] = {map_id: robot.get_map(map_id) for map_id in app.config['MAP_LIST']}
    app.config['CURR_MAP_ID'] = app.config['MAP_LIST'][0] if app.config['MAP_LIST'] else None


    # Enable CORS (Allows frontend to communicate with backend)
    CORS(app)

    # Register all routes
    register_routes(app)

    return app
