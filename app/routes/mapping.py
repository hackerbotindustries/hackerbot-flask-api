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
# This script contains the mapping API endpoints.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from flask import Blueprint, jsonify, current_app, request

bp = Blueprint('mapping_data', __name__)

# Initialize storage dictionaries
map_data_db = {}
markers_db = {}

@bp.route('/api/getml', methods=['GET'])
def get_map_list():        
    map_list = current_app.config['MAP_LIST']
    return jsonify({"map_list": map_list})

@bp.route('/api/getmap/<int:selected_map_id>', methods=['GET'])
def get_compressed_map_data(selected_map_id):
    if current_app.config['MAP_LIST'] is None:
        return jsonify({"error": "No map list found"}), 200

    if selected_map_id not in current_app.config['MAP_LIST']:
        return jsonify({"error": "Invalid map ID: " + str(selected_map_id)}), 200
        
    if selected_map_id not in map_data_db:
        map_data = current_app.config['MAP_DATA'][selected_map_id]
        if map_data is None:
            robot = current_app.config['ROBOT']
            map_data = robot.get_map(selected_map_id)
            if map_data is None:
                return jsonify({"error": "Map data not found: " + str(selected_map_id)}), 200
        map_data_db[selected_map_id] = map_data
        
    return jsonify({
        "map_id": selected_map_id, 
        "map_data": map_data_db[selected_map_id]
    })

@bp.route('/api/save-markers', methods=['POST'])
def save_markers():
    try:
        data = request.json  # Get JSON data from the frontend
        map_id = data.get("map_id")
        markers = data.get("markers", [])
        
        if map_id is None:
            return jsonify({"error": "map_id is required"}), 200
            
        markers_db[map_id] = markers  # Store markers for specific map_id

        return jsonify({
            "map_id": map_id,
            "markers": markers
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200

@bp.route('/api/load-markers/<int:map_id>', methods=['GET'])
def load_markers(map_id):
    try:
        if map_id not in markers_db:
            return jsonify({
                "map_id": map_id,
                "markers": []
            }), 200
            
        return jsonify({
            "map_id": map_id,
            "markers": markers_db[map_id]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200
