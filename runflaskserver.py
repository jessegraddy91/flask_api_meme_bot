#!/usr/bin/python
# -*- coding: utf-8 -*-
# import os

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, \
    marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class ArticleModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    main_art = db.Column(db.Boolean, nullable=False, default=False)


    # def __repr__(self):
        # return f"article(date = {date}, title = {title}, link = {link}, main_art = {main_art})"

# remove db.create_all() after 1st use it sets up database in a janky way

db.create_all()  # its created now yeehaw

article_put_args = reqparse.RequestParser()
article_put_args.add_argument('date', type=int,
                              help='date of the article is required',
                              required=True)
article_put_args.add_argument('title', type=str,
                              help='title of the article',
                              required=True)
article_put_args.add_argument('link', type=str,
                              help='link on the article', required=True)
article_put_args.add_argument('main_art', type=bool,
                              help='has been main article',
                              required=False)

article_update_args = reqparse.RequestParser()
article_update_args.add_argument('date', type=int,
                                 help='date of the article is required')
article_update_args.add_argument('title', type=str,
                                 help='title of the article is required'
                                 )
article_update_args.add_argument('link', type=str,
                                 help='link on the article is required')
article_update_args.add_argument('main_art', type=bool,
                                 help='has been main article')

resource_fields = {
    'id': fields.Integer,
    'date': fields.Integer,
    'title': fields.String,
    'link': fields.String,
    'main_art': fields.Boolean,
    }


class Article(Resource):

    @marshal_with(resource_fields)
    def get(self, article_id):
        result = ArticleModel.query.filter_by(id=article_id).first()
        if not result:
            abort(404, message='Could not find article with that id')
        return result

    @marshal_with(resource_fields)
    def put(self, article_id):
        args = article_put_args.parse_args()
        result = ArticleModel.query.filter_by(id=article_id).first()
        if result:
            abort(409, message='article id taken...')

        article = ArticleModel(id=article_id, date=args['date'],
                               title=args['title'], link=args['link'],
                               main_art=args['main_art'])
        db.session.add(article)
        db.session.commit()
        return (article, 201)

    @marshal_with(resource_fields)
    def patch(self, article_id):
        args = article_update_args.parse_args()
        result = ArticleModel.query.filter_by(id=article_id).first()
        if not result:
            abort(404, message="article doesn't exist, cannot update")

        if args['date']:
            result.date = args['date']
        if args['title']:
            result.title = args['title']
        if args['link']:
            result.link = args['link']
        if args['main_art']:
            result.link = args['main_art']

        db.session.commit()

        return result


    # def delete(self, article_id):
        # abort_if_article_id_doesnt_exist(article_id)
        # del articles[article_id]
        # return '', 204

class latest_art(Resource):
    def get(self):
        my_dict = {'id': 454,'date': '27102020','title': 'baldurs-gate-3-update-reveals-the-most-romanced-npc/\n','link': 'https://www.pcgamer.com/baldurs-gate-3-update-reveals-the-most-romanced-npc/\n','main_art': 0,}
		return my_dict


api.add_resource(Article, '/article/<int:article_id>')
api.add_resource(latest_art, '/latest-article')

if __name__ == '__main__':
    app.run(debug=True)
