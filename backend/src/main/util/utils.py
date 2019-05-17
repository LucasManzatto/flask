from flask_restplus import abort

SUCCESS = 200
CREATED = 201
BAD_REQUEST = 400
NOT_FOUND = 404
CONFLICT = 409


def not_found(response):
    return response.status_code == NOT_FOUND


def success(response):
    return response.status_code == SUCCESS


def bad_request(response):
    return response.status_code == BAD_REQUEST


def conflict(response):
    return response.status_code == CONFLICT


def created(response):
    return response.status_code == CREATED


def message(response, msg):
    return response.json['message'] == msg


def response_created(msg):
    response_object = {
        'status': 'created',
        'message': msg
    }
    return response_object, 201


def response_success(msg):
    response_object = {
        'status': 'success',
        'message': msg
    }
    return response_object, 200


def response_conflict(msg):
    response_object = {
        'status': 'confict',
        'message': msg,
    }
    return response_object, 409


def response_bad_request(msg):
    return abort(400, msg)
