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
# This script registers the routes for the Flask application.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from app.routes import status
from app.routes import mapping
from app.routes import action

def register_routes(app):
    app.register_blueprint(status.bp)
    app.register_blueprint(mapping.bp)
    app.register_blueprint(action.bp)
