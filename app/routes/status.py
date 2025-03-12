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
