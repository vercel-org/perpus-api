from http import HTTPStatus
from flask import make_response,jsonify

def ok(data, message):
    response = {
            "code": "200",
            "status": "OK",
            "data": data,
            "message": message
    }
    return make_response(jsonify(response)),HTTPStatus.OK.value

def ok_with_meta(data, meta):
    response = {
            "code": "200",
            "status": "OK",
            "data": data,
            "meta":  {
                "page": meta.page,
                "pages": meta.pages, 
                "limit": meta.per_page,
                "total_count": meta.total,
                "prev_page": meta.prev_num,
                "next_page": meta.next_num,
                "has_prev": meta.has_prev,
                "has_next": meta.has_next,
            }
    }
    return make_response(jsonify(response)),HTTPStatus.OK.value

def created(data, message):
    response = {
            "code": "201",
            "status": "CREATED",
            "data": data,
            "message": message
    }
    return make_response(jsonify(response)),HTTPStatus.CREATED.value

def bad_request(data):
    response = {
        "code": "400",
        "status": "BAD_REQUEST",
        "message": data
    }
    return make_response(jsonify(response)),HTTPStatus.BAD_REQUEST.value

def bad_request_array(data, message):
    response = {
        "code": "400",
        "status": "BAD_REQUEST",
        "message": {data:[message]}
    }
    return make_response(jsonify(response)),HTTPStatus.BAD_REQUEST.value

def conflict(data):
    response = {
        "code": "409",
        "status": "CONFLICT",
        "message": data
    }
    return make_response(jsonify(response)),HTTPStatus.CONFLICT.value

def conflict_array(data,message):
    response = {
        "code": "409",
        "status": "CONFLICT",
        "message": {data:[message]}
    }
    return make_response(jsonify(response)),HTTPStatus.CONFLICT.value
 
def bad_gateway(data):
    response = {
        "code": "500",
        "status": "BAD_GATEWAY",
        "message": data
    }
    return make_response(jsonify(response)),HTTPStatus.BAD_GATEWAY.value

def forbidden(data):
    return make_response(jsonify(data)),HTTPStatus.FORBIDDEN.value

def unautorized():
    response = {
        "code": "401",
        "status": "UNAUTHORIZED",
        "message": "You are Not Allowed Here"
    }
    return make_response(jsonify(response)),HTTPStatus.UNAUTHORIZED.value

def unautorized_array(data,message):
    response = {
        "code": "401",
        "status": "UNAUTHORIZED",
        "message": {data:[message]}
    }
    return make_response(jsonify(response)),HTTPStatus.UNAUTHORIZED.value

def not_found(data):
    response = {
        "code": "404",
        "status": "NOT_FOUND",
        "message": data
    }
    return make_response(jsonify(response)),HTTPStatus.NOT_FOUND.value

def not_found_array(data, message):
    response = {
        "code": "404",
        "status": "NOT_FOUND",
        "message": {data:[message]}
    }
    return make_response(jsonify(response)),HTTPStatus.NOT_FOUND.value