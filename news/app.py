#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, abort
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/news'
db = SQLAlchemy(app)
JSON_DIR = '../files'

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts'\
            , lazy = 'dynamic'))
    content = db.Column(db.Text)

    def __init__(self, title, created_time, category, content):
        
        self.created_time = created_time 
        self.title = title
        self.category = category
        self.content = content

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

def read_file():
    titles=[]
    json_files = [ anyfile for anyfile in os.listdir(JSON_DIR) \
            if anyfile.endswith('.json') ]
    for json_file in json_files:
        with open(os.path.join(JSON_DIR, json_file)) as f:
            data = json.load(f)
            titles.append(data['title'])
    return titles

@app.route('/')
def index():
    titles = {}
    files = File.query.all()
    for file in files:
        titles[file.id]=file.title
    return render_template('index.html', titles=titles)

@app.route('/files/<file_id>')
def file(file_id):
    the_file = File.query.filter_by(id = file_id).first()
    title = the_file.title
    category = the_file.category
    created_time = the_file.created_time
    content = the_file.content
    return render_template('file.html', title=title, category=category, created_time=created_time, content=content)

@app.errorhandler(404)
def not_found(err):
    return render_template('404.html'), 404

if __name__=='__main__':
    app.run(port=3000, debug=True)

