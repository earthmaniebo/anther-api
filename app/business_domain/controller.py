from .model import BusinessDomain, db_session
from ..business_area.model import BusinessArea
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask import jsonify, Blueprint, request
from app.database import db_session, Base

BusinessDomainController = Blueprint('BusinessDomainController', __name__)

### Create Business Domain
@BusinessDomainController.route('/anther/api/business-domain', methods = ['POST'])
def create_business_domain():
    try:
        # nullables
        general_comment = None
        example_of_use = None

        name = request.json['name']
        business_area_id = request.json['business_area_id']
        if 'general_comment' in request.json:
            general_comment = request.json['general_comment']
        if 'example_of_use' in request.json:
            example_of_use = request.json['example_of_use']

        # Get the business area using id
        business_area = BusinessArea.query.get(int(business_area_id))

        business_domain = BusinessDomain(name, general_comment, example_of_use, business_area)
        db_session.add(business_domain)
        db_session.commit()
        return jsonify(business_domain.serialize), 201

    except KeyError as ke:
        db_session.rollback()
        return jsonify({'error': "The attribute '" + ke.args[0] + "' is required."}), 500

    except IntegrityError as ie:
        db_session.rollback()
        error = ie.args[0].split(':')
        return jsonify({'error': error[1].strip()}), 500


### Get All Business Domain
@BusinessDomainController.route('/anther/api/business-domain', methods = ['GET'])
def get_all_business_domain():
    business_domains = BusinessDomain.query.all()
    return jsonify([i.serialize for i in business_domains]), 200


### Get One Business Domain
@BusinessDomainController.route('/anther/api/business-domain/<int:business_domain_id>', methods=['GET'])
def get_business_domain(business_domain_id):
    business_domain = BusinessDomain.query.filter_by(id=business_domain_id).first()
    if business_domain == None:
        return jsonify({'error': "Business domain doesn't exists."}), 404
    else:
        return jsonify(business_domain.serialize), 200


### Update Business Domain
@BusinessDomainController.route('/anther/api/business-domain/<int:business_domain_id>', methods=['PUT'])
def update_business_domain(business_domain_id):
    business_domain = BusinessDomain.query.filter_by(id=business_domain_id).first()
    if business_domain is None:
        return jsonify({'error': "Business domain doesn't exists."}), 404
    else:
        try:
            name = request.json['name']
            business_domain.name = name
            business_area_id = request.json['business_area_id']
            if 'general_comment' in request.json:
                general_comment = request.json['general_comment']
                business_domain.general_comment = general_comment
            if 'example_of_use' in request.json:
                example_of_use = request.json['example_of_use']
                business_domain.example_of_use = example_of_use

            # Get the business area using id
            business_area = BusinessArea.query.get(int(business_area_id))
            business_domain.business_area = business_area

            db_session.commit()
            return jsonify(business_domain.serialize), 200

        except KeyError as ke:
            db_session.rollback()
            return jsonify({'error': "The attribute '" + ke.args[0] + "' is required."}), 500

        except IntegrityError as ie:
            db_session.rollback()
            error = ie.args[0].split(':')
            return jsonify({'error': error[1].strip()}), 500


### Delete Business Domain
@BusinessDomainController.route('/anther/api/business-domain/<int:business_domain_id>', methods=['DELETE'])
def delete_business_domain(business_domain_id):
    try:
        business_domain = BusinessDomain.query.filter_by(id=business_domain_id).first()

        db_session.delete(business_domain)
        db_session.commit()
        return jsonify({'message': 'Business domain deleted.'}), 200

    except UnmappedInstanceError:
        db_session.rollback()
        return jsonify({'error': "The business domain you are trying to delete doesn't exists."}), 404
