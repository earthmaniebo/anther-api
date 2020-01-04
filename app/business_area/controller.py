from .model import BusinessArea, db_session
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask import jsonify, abort, request, make_response, url_for, Response, json, Blueprint
from bson.json_util import dumps
from app.database import db_session, Base

BusinessAreaController = Blueprint('BusinessAreaController', __name__)

### Create Business Area
@BusinessAreaController.route('/anther/api/business-area', methods = ['POST'])
def create_business_area():
    try:
        name = request.json['name']
        description = None
        if 'description' in request.json:
            description = request.json['description']
        business_area = BusinessArea(name, description)
        db_session.add(business_area)
        db_session.commit()
        if business_area.name != '':
            return jsonify(business_area.serialize), 201

    except KeyError as ke:
        db_session.rollback()
        return jsonify({'error': "The attribute '" + ke.args[0] + "' is required."}), 500

    except IntegrityError as ie:
        db_session.rollback()
        error = ie.args[0].split(':')
        return jsonify({'error': error[1].strip()}), 500


### Get All Business Area
@BusinessAreaController.route('/anther/api/business-area', methods = ['GET'])
def get_all_business_area():
    business_areas = BusinessArea.query.all()
    return jsonify([i.serialize for i in business_areas]), 200


### Get One Business Area
@BusinessAreaController.route('/anther/api/business-area/<int:business_area_id>', methods=['GET'])
def get_business_area(business_area_id):
    business_area = BusinessArea.query.filter_by(id=business_area_id).first()
    if business_area == None:
        return jsonify({'error': "Business area doesn't exists."}), 404
    else:
        return jsonify(business_area.serialize), 200


### Update Business Area
@BusinessAreaController.route('/anther/api/business-area/<int:business_area_id>', methods=['PUT'])
def update_business_area(business_area_id):
    business_area = BusinessArea.query.filter_by(id=business_area_id).first()
    if business_area is None:
        return jsonify({'error': "Business area doesn't exists."}), 404
    else:
        try:
            name = request.json['name']
            business_area.name = name
            if 'description' in request.json:
                description = request.json['description']
                business_area.description = description

            db_session.commit()
            return jsonify(business_area.serialize), 200

        except KeyError as ke:
            db_session.rollback()
            return jsonify({'error': "The attribute '" + ke.args[0] + "' is required."}), 500

        except IntegrityError as ie:
            db_session.rollback()
            error = ie.args[0].split(':')
            return jsonify({'error': error[1].strip()}), 500


### Delete Business Area
@BusinessAreaController.route('/anther/api/business-area/<int:business_area_id>', methods=['DELETE'])
def delete_business_area(business_area_id):
    try:
        business_area = BusinessArea.query.filter_by(id=business_area_id).first()

        db_session.delete(business_area)
        db_session.commit()
        return jsonify({'message': 'Business area deleted.'}), 200

    except UnmappedInstanceError:
        db_session.rollback()
        return jsonify({'error': "The business area you are trying to delete doesn't exists."}), 404
