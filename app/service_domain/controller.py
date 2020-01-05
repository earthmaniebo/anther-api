from .model import ServiceDomain, db_session
from ..business_domain.model import BusinessDomain
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask import jsonify, Blueprint, request
from app.database import db_session, Base

ServiceDomainController = Blueprint('ServiceDomainController', __name__)

### Create Service Domain
@ServiceDomainController.route('/anther/api/service-domain', methods = ['POST'])
def create_service_domain():
    try:
        # nullables
        general_comment = None
        example_of_use = None

        name = request.json['name']
        business_domain_id = request.json['business_domain_id']
        if 'general_comment' in request.json:
            general_comment = request.json['general_comment']
        if 'example_of_use' in request.json:
            example_of_use = request.json['example_of_use']

        # Get the business domain using id
        business_domain = BusinessDomain.query.get(int(business_domain_id))

        service_domain = ServiceDomain(name, general_comment, example_of_use, business_domain)
        db_session.add(service_domain)
        db_session.commit()
        return jsonify(service_domain.serialize), 201

    except KeyError as ke:
        db_session.rollback()
        return jsonify({'error': "The attribute '" + ke.args[0] + "' is required."}), 500

    except IntegrityError as ie:
        db_session.rollback()
        error = ie.args[0].split(':')
        return jsonify({'error': error[1].strip()}), 500


### Get All Service Domain
@ServiceDomainController.route('/anther/api/service-domain', methods = ['GET'])
def get_all_business_domain():
    service_domains = ServiceDomain.query.all()
    return jsonify([i.serialize for i in service_domains]), 200


### Get One Service Domain
@ServiceDomainController.route('/anther/api/service-domain/<int:service_domain_id>', methods=['GET'])
def get_service_domain(service_domain_id):
    service_domain = ServiceDomain.query.filter_by(id=service_domain_id).first()
    if service_domain == None:
        return jsonify({'error': "Service domain doesn't exists."}), 404
    else:
        return jsonify(service_domain.serialize), 200


### Update Service Domain
@ServiceDomainController.route('/anther/api/service-domain/<int:service_domain_id>', methods=['PUT'])
def update_service_domain(service_domain_id):
    service_domain = ServiceDomain.query.filter_by(id=service_domain_id).first()
    if service_domain is None:
        return jsonify({'error': "Service domain doesn't exists."}), 404
    else:
        try:
            name = request.json['name']
            service_domain.name = name
            business_domain_id = request.json['business_domain_id']
            if 'general_comment' in request.json:
                general_comment = request.json['general_comment']
                service_domain.general_comment = general_comment
            if 'example_of_use' in request.json:
                example_of_use = request.json['example_of_use']
                service_domain.example_of_use = example_of_use

            # Get the business domain using id
            business_domain = BusinessDomain.query.get(int(business_domain_id))
            service_domain.business_domain = business_domain

            db_session.commit()
            return jsonify(service_domain.serialize), 200

        except KeyError as ke:
            db_session.rollback()
            return jsonify({'error': "The attribute '" + ke.args[0] + "' is required."}), 500

        except IntegrityError as ie:
            db_session.rollback()
            error = ie.args[0].split(':')
            return jsonify({'error': error[1].strip()}), 500


### Delete Service Domain
@ServiceDomainController.route('/anther/api/service-domain/<int:service_domain_id>', methods=['DELETE'])
def delete_service_domain(service_domain_id):
    try:
        service_domain = ServiceDomain.query.filter_by(id=service_domain_id).first()

        db_session.delete(service_domain)
        db_session.commit()
        return jsonify({'message': 'Service domain deleted.'}), 200

    except UnmappedInstanceError:
        db_session.rollback()
        return jsonify({'error': "The service domain you are trying to delete doesn't exists."}), 404
