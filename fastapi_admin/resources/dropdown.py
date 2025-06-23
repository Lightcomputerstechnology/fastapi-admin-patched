from .base import Resource

class Dropdown(Resource):
    def __init__(self, resources=None):
        self.resources = resources or []
        super().__init__()
