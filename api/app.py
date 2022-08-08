import json
import pytz
from datetime import datetime
from mongo_client import get_db_client

client = get_db_client()
db = client.form_db

def list_data(event, context):
    body = event.get('queryStringParameters', {})
    if not body:
        body = {}
    keyword = body.get('keyword', '')
    limit = body.get('limit', 50)
    skip = body.get('skip', 0)
    sort = json.loads(body.get('sort', '{"name": -1}'))
    query = {}
    or_query = []
    if keyword:
        or_query.append({
            'name': {
                '$regex': keyword,
                '$options': 'i'
            }
        })
        query['$or'] = or_query
    items = list(db.declaration.find(query).limit(int(limit)).skip(int(skip)).sort(list(sort.items())))
    total = db.declaration.count_documents(query)
    result = []
    for item in items:
        result.append({
            '_id': str(item.get('_id')),
            'name': item.get('name'),
            'temperature': item.get('temperature'),
            'hasSymptoms': item.get('hasSymptoms'),
            'hasContactInLast14Days': item.get('hasContactInLast14Days'),
            'createdAt': str(item.get('createdAt', ''))
        })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "result": result,
            "total": total
        })
    }


def submit_form(event, context):
    request_body = event.get('body')
    body = json.loads(request_body)
    name = body.get('name', None)
    temperature = body.get('temperature', None)
    has_symptoms = body.get('hasSymptoms', None)
    has_contact_in_last_14_days = body.get('hasContactInLast14Days', None)

    if name == None or name.strip() == '':
        return {
            "statusCode": 404,
            "body": json.dumps({
                "result": False,
                "message": "Name is required!"
            })
        }

    if len(name.strip()) > 128:
        return {
            "statusCode": 401,
            "body": json.dumps({
                "result": False,
                "message": "Name is too long, max 128 characters!"
            })
        }

    if temperature == None or temperature.strip() == "":
        return {
            "statusCode": 404,
            "body": json.dumps({
                "result": False,
                "message": "Temperature is required!"
            })
        }

    if int(temperature) < 30 or int(temperature) > 45:
        return {
            "statusCode": 401,
            "body": json.dumps({
                "result": False,
                "message": "Temperature is invalid, value must be between 30°C and 45°C!"
            })
        }

    if has_symptoms == None:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "result": False,
                "message": "Option - symtoms checking is required!"
            })
        }

    if has_contact_in_last_14_days == None:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "result": False,
                "message": "Option - contact in last 14 days checking is required!"
            })
        }
    db.declaration.insert({
        "name": name,
        "temperature": temperature,
        "hasSymptoms": has_symptoms,
        "hasContactInLast14Days": has_contact_in_last_14_days,
        "createdAt": datetime.now(pytz.utc)
    })
    return {
        "statusCode": 200,
        "body": json.dumps({
            "result": True,
            "message": "Success"
        })
    }
