from app.routes import status
from app.routes import mapping
from app.routes import action

def register_routes(app):
    app.register_blueprint(status.bp)
    app.register_blueprint(mapping.bp)
    app.register_blueprint(action.bp)
