# # core/server.py

# from flask import jsonify  # 1
# from marshmallow.exceptions import ValidationError  # 2
# from core.libs import helpers  # 3
# from core.libs.exceptions import FyleError  # 4
# from werkzeug.exceptions import HTTPException  # 5
# from sqlalchemy.exc import IntegrityError  # 6

# def register_error_handlers(app):  # 7
#     @app.errorhandler(Exception)  # 8
#     def handle_error(err):  # 9
#         if isinstance(err, FyleError):  # 10
#             return jsonify(error=err.__class__.__name__, message=err.message), err.status_code  # 11
#         elif isinstance(err, ValidationError):  # 12
#             return jsonify(error=err.__class__.__name__, message=err.messages), 400  # 13
#         elif isinstance(err, IntegrityError):  # 14
#             return jsonify(error=err.__class__.__name__, message=str(err.orig)), 400  # 15
#         elif isinstance(err, HTTPException):  # 16
#             return jsonify(error=err.__class__.__name__, message=str(err)), err.code  # 17
#         else:  # 18
#             return jsonify(error="InternalServerError", message=str(err)), 500  # 19

#     @app.route('/')  # 20
#     def ready():  # 21
#         return jsonify({  # 22
#             'status': 'ready',
#             'time': helpers.get_utc_now()
#         })


# core/server.py

from flask import jsonify
from marshmallow.exceptions import ValidationError
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError


from flask import Flask

app = Flask(__name__)


def register_error_handlers(app):
    print("Line 1: register_error_handlers function called")
    
    @app.errorhandler(Exception)
    def handle_error(err):
        print("Line 2: handle_error function called")
        if isinstance(err, FyleError):
            print("Line 3: FyleError handler")
            return jsonify(error=err.__class__.__name__, message=err.message), err.status_code
        elif isinstance(err, ValidationError):
            print("Line 4: ValidationError handler")
            return jsonify(error=err.__class__.__name__, message=err.messages), 400
        elif isinstance(err, IntegrityError):
            print("Line 5: IntegrityError handler")
            return jsonify(error=err.__class__.__name__, message=str(err.orig)), 400
        elif isinstance(err, HTTPException):
            print("Line 6: HTTPException handler")
            return jsonify(error=err.__class__.__name__, message=str(err)), err.code
        else:
            print("Line 7: Default error handler")
            return jsonify(error="InternalServerError", message=str(err)), 500

    @app.route('/')
    def ready():
        print("Line 8: ready function called")
        return jsonify({
            'status': 'ready',
            'time': helpers.get_utc_now()
        })

    print("Line 9: End of register_error_handlers function")