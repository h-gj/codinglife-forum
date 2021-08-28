from flask import jsonify


class StatusCode(object):
    ok = 200
    paramserror = 400
    unautherror = 401
    servererror = 500


def restful_result(code, msg, data):
    return jsonify({'code': code, 'message': msg, 'data': data or {}})


def success(message='', data=None):
    return restful_result(code=StatusCode.ok, msg=message, data=data)


def params_error(message=''):
    return restful_result(code=StatusCode.paramserror, msg=message, data=None)


def server_error(message=''):
    return restful_result(code=StatusCode.servererror, msg=message or 'Internal server error!', data=None)
