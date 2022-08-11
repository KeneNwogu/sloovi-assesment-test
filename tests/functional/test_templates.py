import json
from application import mongo


def test_template_create(client, headers):
    data = {
        "template_name": "My template",
        "subject": "First template",
        "body": "Template body text"
    }
    response = client.post('/template', headers=headers, data=json.dumps(data))
    assert response.status_code == 200


def test_invalid_header(client):
    response = client.post('/template')
    assert response.status_code == 400


def test_all_templates_read(client, headers):
    response = client.get('/template', headers=headers)
    assert response.status_code == 200


def test_single_template_read(client, headers):
    user = mongo.db.users.find_one({'email': 'testuser@gmail.com'})
    template = mongo.db.templates.insert_one({
        "template_name": "My template",
        "subject": "First template",
        "body": "Template body text",
        "user_id": user.get('_id')
    })
    template_id = str(template.inserted_id)
    response = client.get(f'/template/{template_id}', headers=headers)
    assert response.status_code == 200
    mongo.db.templates.drop()


def test_template_edit(client, headers):
    user = mongo.db.users.find_one({'email': 'testuser@gmail.com'})
    template = mongo.db.templates.insert_one({
        "template_name": "My template",
        "subject": "First template",
        "body": "Template body text",
        "user_id": user.get('_id')
    })
    edit_data = {
        "template_name": "My template",
        "subject": "Edited",
    }
    template_id = str(template.inserted_id)
    response = client.put(f'/template/{template_id}', headers=headers, data=json.dumps(edit_data))
    assert response.status_code == 200
    edited_template = mongo.db.templates.find_one({'_id': template.inserted_id})
    assert edited_template.get('subject') == 'Edited'
    mongo.db.templates.drop()


def test_template_delete(client, headers):
    user = mongo.db.users.find_one({'email': 'testuser@gmail.com'})
    template = mongo.db.templates.insert_one({
        "template_name": "My template",
        "subject": "First template",
        "body": "Template body text",
        "user_id": user.get('_id')
    })
    template_id = str(template.inserted_id)
    response = client.delete(f'/template/{template_id}', headers=headers)
    assert response.status_code == 200
    template = mongo.db.templates.find_one({'_id': template.inserted_id})
    assert template is None
    mongo.db.templates.drop()
