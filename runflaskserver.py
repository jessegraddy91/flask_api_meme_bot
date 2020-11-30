from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)


class latest_art(Resource):
    def get(self):
        my_dict = {"id": "454"}
        return my_dict


api.add_resource(latest_art, "/latest-article")

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
