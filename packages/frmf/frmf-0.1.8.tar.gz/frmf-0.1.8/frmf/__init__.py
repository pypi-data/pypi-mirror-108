import traceback

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, MethodNotAllowed, HTTPException

from frmf.api_view import ApiView
from frmf.logic import Logic
from frmf.manager import Manager
from frmf.db_helper import DBHelper
from frmf.response import abort
from frmf.response import make_response
from flask_restful import Api as _Api
from flask_restful.utils import http_status_message


class Api(_Api):
    def handle_error(self, e):
        """It helps preventing writing unnecessary
        try/except block though out the application
        """
        # Handle HTTPExceptions
        if isinstance(e, ValidationError):
            messages = e.normalized_messages()
            for key in messages.keys():
                messages[key] = messages[key][0]
            return make_response(False, messages, 400)
        elif isinstance(e, BadRequest):
            return make_response(False, e.data.get('message'), e.code)
        elif isinstance(e, MethodNotAllowed):
            return make_response(False, {'error': http_status_message(e.code)}, e.code)
        elif isinstance(e, AppException):
            return make_response(False, e.payload, e.status_code)
        else:
            traceback.print_exc()

        if isinstance(e, HTTPException):
            if hasattr(e, 'description') and e.description is not None:
                return make_response(False, getattr(e, 'description'), e.code)
        if isinstance(e, IntegrityError):
            if e.orig.args[0] == 1062:
                return make_response(False, {'error': http_status_message(409)}, 409)
            elif e.orig.args[0] == 1451:
                return make_response(False, {'error': http_status_message(409)}, 409)
        return make_response(False, {'error': http_status_message(409)}, 500)


class AppException(Exception):
    status_code = 500

    def __init__(self, payload=None, status_code=None):
        super(BaseException, self).__init__()
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return dict(self.payload or ())
