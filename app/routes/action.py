from flask import Blueprint, jsonify, current_app

bp = Blueprint('action', __name__)

@bp.route('/api/ping/', methods=['GET'])
def ping_command():
    robot = current_app.config['ROBOT']
    result = robot.get_ping()
    if result:
        return jsonify({'response': result})
    return jsonify({'error': robot.get_error()})

@bp.route('/api/version/', methods=['GET'])
def version_command():
    robot = current_app.config['ROBOT']
    result = robot.get_versions()
    if result:
        return jsonify({'response': result})
    return jsonify({'error': robot.get_error()})

@bp.route('/api/stop/', methods=['GET'])
def stop_command():
    robot = current_app.config['ROBOT']
    result = robot.stop_driver()
    if result:
        return jsonify({'response': 'STOP Command Successful'})
    return jsonify({'error': robot.get_error()})

@bp.route('/api/machine/<param>', methods=['POST'])
def machine_command(param):
    robot = current_app.config['ROBOT']
    result = False
    if param == '1':
        result = robot.activate_machine_mode()
    elif param == '0':
        result = robot.deactivate_machine_mode()
    if result:
        return jsonify({'response': 'MACHINE Command Successful'})
    return jsonify({'error': robot.get_error()})

@bp.route('/api/init/', methods=['GET'])
def init_command():
    robot = current_app.config['ROBOT']
    result = robot.init_driver()
    if result:
        return jsonify({'response': 'INIT Command Successful'})
    return jsonify({'error': robot.get_error()})

@bp.route('/api/goto/<param>', methods=['POST'])
def goto_command(param):
    try:
        values = [int(x) for x in param.split(",")]
        robot = current_app.config['ROBOT']
        x_coord = values[0]
        y_coord = values[1]
        angle = values[2]
        speed = values[3]

        result = robot.goto_pos(x_coord, y_coord, angle, speed)
        if result:
            return jsonify({'response': 'GOTO Command Successful'})
        return jsonify({'error': robot.get_error()})
    except Exception as e:
        return jsonify({'error': str(e)})

@bp.route('/api/enter/', methods=['GET'])
def enter_command():
    robot = current_app.config['ROBOT']
    result = robot.leave_base()
    if result:
        return jsonify({'response': 'Enter Command Successful'})
    return jsonify({'error': robot.get_error()})

@bp.route('/api/dock/', methods=['GET'])
def dock_command():
    robot = current_app.config['ROBOT']
    result = robot.dock()
    if result:
        return jsonify({'response': 'DOCK Command Successful'})
    return jsonify({'error': robot.get_error()})

@bp.route('/api/quickmap/', methods=['GET'])
def quickmap_command():
    robot = current_app.config['ROBOT']
    result = robot.quickmap()
    if result:
        return jsonify({'response': 'QUICKMAP Command Successful'})
    return jsonify({'error': robot.get_error()})