from flask import jsonify

class InvalidUsageError(Exception):  # custom exception class

    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        dict_ = {}
        dict_['response'] = self.message
        dict_['status code'] = self.status_code
        return dict_

class InternalServerError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    }
}