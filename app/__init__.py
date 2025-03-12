from flask import Flask, g
from flask_cors import CORS
from app.routes import register_routes
import hackerbot_helper as hhp


# def connect_robot():
#     if not hasattr(g, 'robot'):  # Ensure the robot is connected only once
#         g.robot = hhp.ProgrammedController()
#         g.robot.init_driver()
#         g.map_list = g.robot.get_map_list()
#         g.map_data = g.robot.get_map(g.map_list[0])
#         g.curr_map_id = g.map_list[0] if len(g.map_list) > 0 else None


def create_app():
    app = Flask(__name__)

    # app.before_request(connect_robot)

    # Load configuration
    app.config.from_object('app.config.Config')

    # Create a single controller instance
    robot = hhp.ProgrammedController()
    robot.init_driver()
    
    # Store everything in app.config
    app.config['ROBOT'] = robot
    app.config['MAP_LIST'] = robot.get_map_list()
    app.config['MAP_DATA'] = robot.get_map(app.config['MAP_LIST'][0]) if app.config['MAP_LIST'] else None
    app.config['CURR_MAP_ID'] = app.config['MAP_LIST'][0] if app.config['MAP_LIST'] else None


    # Enable CORS (Allows frontend to communicate with backend)
    CORS(app)

    # Register all routes
    register_routes(app)

    return app
