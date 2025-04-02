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
# This script contains the status API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from flask import Blueprint, jsonify, current_app

bp = Blueprint('status', __name__)

@bp.route('/api/status', methods=['GET'])
def get_status():
    robot = current_app.config['ROBOT']
    status = robot.get_current_action()
    return jsonify({"status": status})

@bp.route('/api/error', methods=['GET'])
def get_error():
    robot = current_app.config['ROBOT']
    error = robot.get_error()
    return jsonify({"error": error})
