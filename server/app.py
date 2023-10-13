#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


@app.get('/scientists')
def get_scientists():
    response_dict = [s.to_dict(only=('id', 'name', 'field_of_study'))
                     for s in Scientist.query.all()]
    return make_response(response_dict, 200)


@app.get('/scientists/<int:id>')
def get_scientists_by_id(id):
    sci = Scientist.query.filter_by(id=id).first()

    if not sci:
        return make_response({"error": "scientist not found"}, 404)

    return make_response(sci.to_dict(), 200)


@app.post('/scientists')
def post_scientists():
    data = request.get_json()
    try:
        new_scientist = Scientist(
            name=data['name'],
            field_of_study=data['field_of_study']
        )
    except Exception:
        return make_response({"errors": ["validation errors"]}, 422)
    db.session.add(new_scientist)
    db.session.commit()
    return make_response(new_scientist.to_dict(only=("id", 'name', 'field_of_study')), 201)


@app.patch('/scientists/<int:id>')
def patch_scientists(id):
    sci = Scientist.query.filter_by(id=id).first()
    data = request.get_json()

    if not sci:
        return make_response({"error": "Scientist not found"}, 404)

    try:
        for field in data:
            setattr(sci, field, data[field])
    except:
        return make_response({"errors": ["validation errors"]}, 422)

    db.session.commit()
    return make_response(sci.to_dict(rules=('-mission_s_relationship',)), 202)


@app.delete('/scientists/<int:id>')
def delete_scientists(id):
    sci = Scientist.query.filter_by(id=id).first()

    if not sci:
        return make_response({"error": "Scientist not found"}, 404)

    db.session.delete(sci)
    db.session.commit()

    return make_response({"message": "This rizz was deleted by tri, you punk"}, 226)


@app.get('/planets')
def get_planets():
    response_dict_list = [p.to_dict() for p in Planet.query.all()]
    return make_response(response_dict_list, 200)


@app.get('/missions')
def get_missions():
    response_dict_list = [m.to_dict() for m in Mission.query.all()]
    return make_response(response_dict_list, 200)


@app.post('/missions')
def post_mission():
    request_object = request.get_json()
    try:
        new_mission = Mission(
            name=request_object['name'],
            scientist_id=request_object['scientist_id'],
            planet_id=request_object['planet_id']
        )
        db.session.add(new_mission)
        db.session.commit()
    except Exception as e:
        # different way to show our errors
        message = {'errors': [e.__str__()]}
        return make_response(message, 422)
    return make_response(new_mission.to_dict(), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

# #!/usr/bin/env python3

# from models import db, Scientist, Mission, Planet
# from flask_restful import Api, Resource
# from flask_migrate import Migrate
# from flask import Flask, make_response, jsonify, request
# import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# migrate = Migrate(app, db)

# db.init_app(app)


# @app.route('/')
# def home():
#     return ''


# @app.get('/scientists')
# def get_all_scientists():
#     scientists = Scientist.query.all()
#     data = [scientist.to_dict(rules=('-mission',)) for scientist in scientists]

#     return make_response(
#         jsonify(data),
#         200
#     )


# @app.get('/scientists/<int:id>')
# def set_scientists(id):
#     scientist = Scientist.query.filter(Scientist.id == id).first()

#     if not scientist:
#         return make_response(
#             jsonify({"error": "Scientist not found"}),
#             404
#         )
#     return make_response(
#         jsonify(scientist.to_dict()),
#         200
#     )


# @app.post('/scientists')
# def post_scientists():
#     data = request.get_json()
#     print(data)

#     try:
#         new_scientist = Scientist(
#             name=data['name'],
#             field_of_study=data['field_of_study']
#         )

#     except Exception:
#         return make_response({'errors': ['validation error']}, 422)
#     db.sessions.add(new_scientist)
#     db.session.commit()
#     return make_response(new_scientist.to_dict(), 201)


# # @app.patch('/scientist/<int:id>')
# # def patch_scientist(id):
# #     sci = Scientist.query.filter_by(id=id).first()
# #     data=request.get_json()

# #     if not sci:
# #         return make_response({"error": "BJBHUVUY"},404)

# #     try:
# #         for field in data:
# #             setattr(sci, field, data[field])
# #     except:
# #         return make_response({"error": ["validation error"]


# if __name__ == '__main__':
#     app.run(port=5555, debug=True)
