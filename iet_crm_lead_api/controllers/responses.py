from odoo import http
from odoo.http import request

# Handling Response Structure
def valid_response(message='success', data=None, status=200):
    return request.make_json_response({
        'Message': message,
        'Data': data,
    }, status=status)

def invalid_response(message='Failed', error=None, status=400):
    return request.make_json_response({
        'Message': message,
        'Error': error,
    }, status=status)
