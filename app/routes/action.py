from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('action', __name__)

# -------------------- CORE --------------------
@bp.route('/api/v1/core', methods=['POST'])
def core_post():
    robot = current_app.config['ROBOT']
    data = request.get_json()
    if not data or 'method' not in data:
        return jsonify({'error': 'Missing method'}), 400

    if data['method'] == 'ping':
        result = robot.core.ping()
    elif data['method'] == 'settings':
        result = True
        if 'json-responses' in data:
            result &= robot.set_json_mode(data['json-responses'])
        if 'tofs-enabled' in data:
            result &= robot.set_TOFs(data['tofs-enabled'])
    else:
        return jsonify({'error': 'Invalid method'}), 400

    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

@bp.route('/api/v1/core/version', methods=['GET'])
def core_version():
    robot = current_app.config['ROBOT']
    result = robot.core.version()
    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

# -------------------- BASE --------------------
@bp.route('/api/v1/base', methods=['POST'])
def base_post():
    robot = current_app.config['ROBOT']
    data = request.get_json()
    if not data or 'method' not in data:
        return jsonify({'error': 'Missing method'}), 400

    method = data['method']
    if method == 'initialize':
        result = robot.base.initialize()
    elif method == 'mode':
        result = robot.base.set_mode(data.get('mode_id'))
    elif method == 'start':
        result = robot.base.start()
    elif method == 'quickmap':
        result = robot.base.quickmap()
    elif method == 'dock':
        result = robot.base.dock()
    elif method == 'kill':
        result = robot.base.kill()
    elif method == 'trigger-bump':
        result = robot.base.trigger_bump(data.get('left'), data.get('right'))
    elif method == 'speak':
        result = robot.base.speak(data.get('model_src'), data.get('text'), data.get("speaker_id"))
    else:
        return jsonify({'error': 'Invalid method'}), 400

    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

@bp.route('/api/v1/base/status', methods=['GET'])
def base_status():
    robot = current_app.config['ROBOT']
    result = robot.base.status()
    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

@bp.route('/api/v1/base/actions', methods=['POST'])
def base_drive():
    robot = current_app.config['ROBOT']
    data = request.get_json()
    result = robot.base.drive(data.get('linear_velocity'), data.get('angle_velocity'))
    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

@bp.route('/api/v1/base/maps/position', methods=['GET'])
def base_position():
    robot = current_app.config['ROBOT']
    result = robot.base.maps.position()
    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

@bp.route('/api/v1/base/maps', methods=['POST'])
def base_goto():
    robot = current_app.config['ROBOT']
    data = request.get_json()
    method = data.get('method')
    if method == 'goto':
        print(data)
        if data.get('x') is None or data.get('y') is None:
            return jsonify({'error': 'Missing parameters'}), 400
        result = robot.base.maps.goto(data.get('x'), data.get('y'), data.get('angle'), data.get('speed'))
        return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

# -------------------- HEAD --------------------
@bp.route('/api/v1/head', methods=['PUT'])
def head_settings():
    robot = current_app.config['ROBOT']
    data = request.get_json()
    result = robot.head.set_idle_mode(data.get('idle-mode'))
    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

@bp.route('/api/v1/head', methods=['POST'])
def head_command():
    robot = current_app.config['ROBOT']
    data = request.get_json()
    method = data.get('method')

    if method == 'look':
        result = robot.head.look(data.get('yaw'), data.get('pitch'), data.get('speed'))
    elif method == 'gaze':
        result = robot.head.eyes.gaze(data.get('x'), data.get('y'))
    else:
        return jsonify({'error': 'Invalid method'}), 400

    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

@bp.route('/api/v1/head/position', methods=['GET'])
def head_position():
    robot = current_app.config['ROBOT']
    result = robot.head.get_position()
    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

# -------------------- ARM --------------------
@bp.route('/api/v1/arm/gripper', methods=['POST'])
def gripper_command():
    robot = current_app.config['ROBOT']
    data = request.get_json()
    method = data.get('method')

    if method == 'calibrate':
        result = robot.arm.gripper.calibrate()
    elif method == 'open':
        result = robot.arm.gripper.open()
    elif method == 'close':
        result = robot.arm.gripper.close()
    else:
        return jsonify({'error': 'Invalid method'}), 400

    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

@bp.route('/api/v1/arm', methods=['POST'])
def arm_command():
    robot = current_app.config['ROBOT']
    data = request.get_json()
    method = data.get('method')

    if method == 'move-joint':
        result = robot.arm.move_joint(data.get('joint'), data.get('angle'), data.get('speed'))
    elif method == 'move-joints':
        result = robot.arm.move_joints(data.get('angles'), data.get('speed'))
    else:
        return jsonify({'error': 'Invalid method'}), 400

    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})

@bp.route('/api/v1/arm/position', methods=['GET'])
def arm_position():
    robot = current_app.config['ROBOT']
    result = robot.arm.get_position()
    return jsonify({'response': result}) if result else jsonify({'error': robot.get_error()})
