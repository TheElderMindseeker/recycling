from flask import Blueprint, jsonify, abort
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from geoalchemy2 import func

from src.models import Recycle, TrashPoint

recycles = Blueprint('recycles', __name__)
api = Api(recycles)

geo_rec_parser = reqparse.RequestParser()
recycles_parser = reqparse.RequestParser()

geo_rec_parser.add_argument('center', type=str, required=True)
geo_rec_parser.add_argument('radius', type=float, required=True)
geo_rec_parser.add_argument('trash_types', type=str)

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
        args = geo_rec_parser.parse_args()
        ids = Recycle.query.filter(
            func.ST_Distance_Sphere(args['center'], Recycle.position) <=
            args['radius'])
        result = ids.all()
        if args['trash_types']:
            result = [
                r_obj.id for r_obj in result
                if set(args['trash_types'].split(',')).issubset(
                    set(r_obj.trash_types.split('&')))
            ]
            return {'ids': result}
        else:
            return {'ids': [r_obj.id for r_obj in result]}

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
        print(new_recycle.id)
        return {'id': new_recycle.id}


recycle_fields = {
    'name': fields.String,
    'address': fields.String,
    'position': fields.String,
    'open_time': fields.String,
    'close_time': fields.String,
    'trash_types': fields.String,
    'bonus_program': fields.Boolean,
}


class Recycles(Resource):
    """Individual resources"""
    @marshal_with(recycle_fields)
    def get(self, rec_id):
        """Get recycle info by id"""
        got_recycle = Recycle.query.get(rec_id)
        if not got_recycle:
            abort(404)

        return got_recycle

    def put(self, rec_id):
        """Update recycle by id"""
        pass

    def delete(self, rec_id):
        """Delete recycle with specified id"""


trash_point_parser = reqparse.RequestParser()
trash_point_parser.add_argument('address', type=str, required=True)
trash_point_parser.add_argument('position', type=str, required=True)
trash_point_parser.add_argument('comment', type=str, required=True)
trash_point_parser.add_argument('contacts', type=str, required=True)
trash_point_parser.add_argument('trash_types', type=str, required=True)


class TrashPointsList(Resource):
    """List of trash points"""
    def get(self):
        """Get all trash points available"""
        args = geo_rec_parser.parse_args()
        ids = TrashPoint.query.filter(
            func.ST_Distance_Sphere(args['center'], TrashPoint.position) <=
            args['radius'])
        result = ids.all()
        if args['trash_types']:
            result = [
                r_obj.id for r_obj in result
                if set(args['trash_types'].split(',')).issubset(
                    set(r_obj.trash_types.split('&')))
            ]
            return {'ids': result}
        else:
            return {'ids': [r_obj.id for r_obj in result]}

    def post(self):
        """Create a new trash point"""
        args = trash_point_parser.parse_args()
        new_trash_point = TrashPoint(address=args['address'],
                                     position=args['position'],
                                     comment=args['comment'],
                                     contacts=args['contacts'],
                                     trash_types=args['trash_types'])
        new_trash_point.save()
        return dict()


trash_point_fields = {
    'position': fields.String,
    'comment': fields.String,
    'address': fields.String,
    'contacts': fields.String,
    'trash_types': fields.String,
}


class TrashPoints(Resource):
    """Individual trash points"""
    @marshal_with(trash_point_fields)
    def get(self, tr_id):
        """Get trash point info"""
        trash_point_got = TrashPoint.query.get(tr_id)
        if not trash_point_got:
            abort(404)

        return trash_point_got


api.add_resource(RecyclesList, '/recycles')
api.add_resource(Recycles, '/recycles/<int:rec_id>')
api.add_resource(TrashPointsList, '/trashpoints')
api.add_resource(TrashPoints, '/trashpoints/<int:tr_id>')
