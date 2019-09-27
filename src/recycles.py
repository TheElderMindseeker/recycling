from flask import Blueprint
from flask_restful import Api, Resource, reqparse

from src.models import Recycle

recycles = Blueprint('recycles', __name__)
api = Api(recycles)


recycles_parser = reqparse.RequestParser()

recycles_parser.add_argument('name', type=str, required=True)
recycles_parser.add_argument('address', type=str, required=True)
recycles_parser.add_argument('position', type=str, required=True)
recycles_parser.add_argument('open_time', type=str, required=True)
recycles_parser.add_argument('close_time', type=str, required=True)
recycles_parser.add_argument('trash_types', type=str, required=True)
recycles_parser.add_argument('bonus_program', type=bool, required=True)


class RecyclesList(Resource):
    """List of recycle units"""
    def get(self):
        """Get list of recycle units"""
    def post(self):
        """Create new recycle unit"""
        args = recycles_parser.parse_args()
        new_recycle = Recycle(
            name=args['name'],
            address=args['address'],
            position=args['position'],
            open_time=args['open_time'],
            close_time=args['close_time'],
            trash_types=args['trash_types'],
            bonus_program=args['bonus_program'],
        )
        new_recycle.save()


api.add_resource(RecyclesList, '/recycles')
