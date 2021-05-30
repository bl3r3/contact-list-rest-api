"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask.globals import g
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Contact, Group

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)



@app.route('/contact/all', methods=['GET'])
def get_contact():
    contacts = Contact.contact_all();
    contact_list_dict = list(map(lambda elem: elem.serialize(), contacts))
    return jsonify(contact_list_dict), 200 


@app.route("/contact", methods=['POST'])
def create_contact():
    """Recibe un nuevo contacto"""
    #request in json
    request_body = request.json

    new_contact = Contact.create(
        full_name = request_body["full_name"],
        email = request_body["email"],
        address = request_body["address"],
        phone = request_body["phone"],
        memberships = request_body["memberships"]
    )

    #Save and commit 
    new_contact.save()
    #Return a response
    return jsonify(new_contact.serialize()), 200



@app.route('/contact/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def contact_by_id(id):
    if request.method == 'DELETE':
        contact = Contact.get_contact_by_id(id);
        contact.delete_contact_by_id(contact);
        response_body = {
            "msg": f"user {id} deleted"
        }
        return jsonify(response_body), 200

    if request.method == 'PUT':
       contact = Contact.query.filter_by(id=id).first();
       request_body = request.json
       contact.full_name =  request_body["full_name"]
       contact.email = request_body["email"]
       contact.address = request_body["address"]
       contact.phone = request_body["phone"]

       contact.save()

       return jsonify(contact.serialize()), 200
    
        
    contact = Contact.get_contact_by_id(id)
    return jsonify(contact.serialize()), 200
    


@app.route('/group/all', methods=['GET'])
def get_all():
    groups = Group.get_all_groups();
    gruop_to_dict = list(map(lambda elem: elem.serialize(), groups))
    return jsonify(gruop_to_dict), 200


@app.route('/group', methods=['POST'])
def create_a_gruop():
    request_body = request.json
    new_group = Group.create(
        name = request_body["name"]
    )
     #Save and commit 
    new_group.save()
    #Return a response
    return jsonify(new_group.serialize()), 200



@app.route('/group/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def gruop_by_id(id):
    if request.method == 'DELETE':
        group = Group.get_group_by_id(id)
        group.delete_group_by_id(group)
        response_body = {
            "msg": f"group {id} deleted"
        }
        return jsonify(response_body), 200

    if request.method == 'PUT':
       group = Group.query.filter_by(id=id).first();
       request_body = request.json
       group.name =  request_body["name"]

       group.save()

       return jsonify(group.serialize()), 200


    group = Group.get_group_by_id(id)
    return jsonify(group.serialize()), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
