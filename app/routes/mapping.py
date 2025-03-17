from flask import Blueprint, jsonify, current_app

bp = Blueprint('mapping_data', __name__)

@bp.route('/api/getml', methods=['GET'])
def get_map_list():        
    map_list = current_app.config['MAP_LIST']
    return jsonify({"map_list": map_list})

@bp.route('/api/getmap/<int:selected_map_id>', methods=['GET'])
def get_compressed_map_data(selected_map_id):
    robot = current_app.config['ROBOT']
    map_data = current_app.config['MAP_DATA']
    curr_map_id = current_app.config['CURR_MAP_ID']

    if selected_map_id != curr_map_id:
        current_app.config['CURR_MAP_ID'] = selected_map_id
        map_data = robot.get_map(selected_map_id)
        print("Fetched new map data for", selected_map_id)
        
    return jsonify({"map_id": selected_map_id, "map_data": map_data})