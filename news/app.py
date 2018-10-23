#!/usr/bin/env python3
from flask import Flask, render_template, abort
import os
import json

app = Flask(__name__)
JSON_DIR = '../files'

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
    titles = read_file()
    return render_template('index.html', titles=titles)

@app.route('/files/<filename>')
def file(filename):
    data = {}
    json_path = os.path.join(JSON_DIR, '{}.json'.format(filename))
    if not os.path.isfile(json_path):
        abort(404)
    else:
        with open(json_path) as f:
            data = json.load(f)
    return render_template('file.html', data = data)

@app.errorhandler(404)
def not_found(err):
    return render_template('404.html'), 404

if __name__=='__main__':
    app.run(port=3000, debug=True)

