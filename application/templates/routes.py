from bson import ObjectId
from flask import Blueprint, request
from marshmallow import ValidationError

from application import mongo
from application.api.auth import login_required
from application.api.errors import resource_not_found, bad_request, unauthorised
from application.serializers import TemplatesSerializer

templates = Blueprint('templates', __name__)


@templates.route('/template', methods=['GET'])
@login_required
def get_all_templates(user):
    templates_data = list(mongo.db.templates.find({'user_id': user.get('_id')}))
    template_schema = TemplatesSerializer(many=True)
    return template_schema.dump(templates_data, many=True)


@templates.route('/template', methods=['POST'])
@login_required
def create_template(user):
    data = request.get_json()
    template_schema = TemplatesSerializer()
    try:
        template_data = template_schema.load(data)
    except ValidationError:
        return bad_request("Invalid template data provided")
    template_data['user_id'] = user.get('_id')
    mongo.db.templates.insert_one(template_data)
    return {"success": True, "message": "successfully created template", "template_id": str(template_data.get('_id'))}


@templates.route('/template/<template_id>', methods=['GET'])
@login_required
def get_template(user, template_id):
    template_data = mongo.db.templates.find_one({'user_id': user.get('_id'), '_id': ObjectId(template_id)})
    if template_data:
        template_schema = TemplatesSerializer()
        return template_schema.dump(template_data)
    else:
        return resource_not_found('Template not found')


@templates.route('/template/<template_id>', methods=['PUT'])
@login_required
def update_template(user, template_id):
    data = request.get_json()
    template_schema = TemplatesSerializer()
    try:
        template_data = template_schema.load(data)
    except ValidationError:
        return bad_request('Invalid template data was provided')
    template = mongo.db.templates.find_one({"_id": ObjectId(template_id)})
    if template:
        if template.get('user_id') != user.get('_id'):
            return unauthorised("Template you are trying to update does not belong to logged in user")
        mongo.db.templates.update_one({"_id": ObjectId(template_id)}, {"$set": template_data})
        return {"success": True, "message": "successfully updated template"}
    else:
        return resource_not_found("Template you are trying to update does not exist")


@templates.route('/template/<template_id>', methods=['DELETE'])
@login_required
def delete_template(user, template_id):
    template = mongo.db.templates.find_one({"_id": ObjectId(template_id)})
    if template:
        if template.get('user_id') != user.get('_id'):
            return unauthorised("Template you are trying to delete does not belong to logged in user")
        mongo.db.templates.delete_one({"_id": ObjectId(template_id)})
        return {"success": True, "message": "successfully deleted template"}
    else:
        return resource_not_found("Template you are trying to delete does not exist")
