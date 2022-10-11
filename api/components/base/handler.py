from api.config.auth import token_required, has_permissions
from api.utils import logger
from flask_restful import Resource


class Index(Resource):
    @staticmethod
    def get():
        return "iTask Restful API!"
