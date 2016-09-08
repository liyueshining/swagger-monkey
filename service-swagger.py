from flask import Flask, g, jsonify, flash, redirect, url_for
from flask import request
from flask_swagger import swagger
from flask_cors import CORS, cross_origin
import sqlite3
from contextlib import closing

import logging
import logging.config
import os

LOGGER_CONF_FILE = "logger.conf"
LOGGER_DATA_DIR = "log"

if os.path.exists(LOGGER_DATA_DIR) is False:
    os.mkdir(LOGGER_DATA_DIR)
logging.config.fileConfig(LOGGER_CONF_FILE)
logger = logging.getLogger("rotatingFile")


#configuration
DATABASE = 'swagger-monkey.db'

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)


@app.route('/urls', methods=['GET'])
def urls_get_service():
    """
    get all url infos
    ---
    tags:
      - urls
    definitions:
      - schema:
          id: UrlInfo
          required:
            - key
            - title
            - url
            - description
            - vote
          properties:
                key:
                  type: integer
                  description: auto increment id
                title:
                  type: string
                  description: title of url
                url:
                  type: string
                  description: http url
                description:
                  type: string
                  description: describe the url
                vote:
                  type: integer
                  description: counter of clicking
    responses:
      200:
        description: Returns a list of url infos
        schema:
            $ref: '#/definitions/UrlInfo'
    """
    try:
        infos = query_db("select * from urlinfos")
        if infos is None:
            flash("no url to get")
        urls = []
        for info in infos:
            url = {}
            url['key'] = int(info[0])
            url['title'] = info[1]
            url['url'] = info[2]
            url['description'] = info[3]
            url['vote'] = int(info[4])
            urls.append(url)
        return jsonify(urls)
    except Exception, e:
        return e.message


@app.route('/urls', methods=['POST'])
def urls_post_service():
    """
    Create a new url info
    ---
    tags:
      - urls
    parameters:
      - name: urlinfo
        in: body
        required: true
        schema:
          id: UrlInfo
          required:
            - key
            - title
            - url
            - description
            - vote
          properties:
                key:
                  type: integer
                  description: auto increment id
                title:
                  type: string
                  description: title of url
                url:
                  type: string
                  description: http url
                description:
                  type: string
                  description: describe the url
                vote:
                  type: integer
                  description: counter of clicking
        responses:
          201:
            description: User created
            schema:
                $ref: '#/definitions/UrlInfo'
    """

    try:
        update_db('insert into urlinfos ( title, url, description) values (?, ?, ?)',
                    [request.json['title'], request.json['url'], request.json['description']])

        info = query_db('select * from urlinfos where title = ?', [request.json['title']], one=True)
        url = {}
        url['key'] = int(info[0])
        url['title'] = info[1]
        url['url'] = info[2]
        url['description'] = info[3]
        url['vote'] = int(info[4])
        return jsonify(url)
    except Exception, e:
        return e.message


@app.route('/urls', methods=['DELETE'])
def urls_delete_service():
    """
    delete all url infos
    ---
    tags:
      - urls
    responses:
      200:
        description: all url infos deleted
    """

    try:
        delete_db("delete from urlinfos")
        return 'success'
    except Exception, e:
        return e.message


@app.route('/urls/<int:key>', methods=['GET'])
def url_get_service(key):
    """
    get all url infos
    ---
    tags:
      - urls
    parameters:
      - name: key
        in: path
        required: true
        type: integer
    definitions:
      - schema:
          id: UrlInfo
          required:
            - key
            - title
            - url
            - description
            - vote
          properties:
                key:
                  type: integer
                  description: auto increment id
                title:
                  type: string
                  description: title of url
                url:
                  type: string
                  description: http url
                description:
                  type: string
                  description: describe the url
                vote:
                  type: integer
                  description: counter of clicking
    responses:
          200:
            description: Returns one url info
            schema:
                $ref: '#/definitions/UrlInfo'
    """

    try:
        info = query_db('select * from urlinfos where key = ?', [key], one=True)
        if info is None:
            return 'no such urlinfo'
        else:
            url = {}
            url['key'] = int(info[0])
            url['title'] = info[1]
            url['url'] = info[2]
            url['description'] = info[3]
            url['vote'] = int(info[4])
        return jsonify(url)
    except Exception, e:
        return e.message


@app.route('/urls/<int:key>', methods=['PUT'])
def url_put_service(key):
    """
    Create or update one url info
    ---
    tags:
      - urls
    parameters:
      - name: key
        in: path
        required: true
        type: integer
      - name: urlinfo
        in: body
        required: true
        schema:
          id: UrlInfo
          required:
            - key
            - title
            - url
            - description
            - vote
          properties:
                key:
                  type: integer
                  description: auto increment id
                title:
                  type: string
                  description: title of url
                url:
                  type: string
                  description: http url
                description:
                  type: string
                  description: describe the url
                vote:
                  type: integer
                  description: counter of clicking
        responses:
          201:
            description: Url info created or updated
            schema:
                $ref: '#/definitions/UrlInfo'
    """

    try:
        update_db('update urlinfos set title = ?, url = ?, description = ?, vote = ? where key = ?',
                        [request.json['title'], request.json['url'], request.json['description'], int(request.json['vote']),
                         key])

        info = query_db('select * from urlinfos where key = ?', [key], one=True)
        if info is None:
            flash('no such urlinfo')
        else:
            url = {}
            url['key'] = int(info[0])
            url['title'] = info[1]
            url['url'] = info[2]
            url['description'] = info[3]
            url['vote'] = int(info[4])
        return jsonify(url)
    except Exception, e:
        return e.message


@app.route('/urls/<int:key>', methods=['DELETE'])
def url_delete_service(key):
    """
    delete one url
    ---
    tags:
      - urls
    parameters:
      - name: key
        in: path
        required: true
        type: integer
    responses:
      200:
        description: one url info deleted
    """

    try:
        delete_db('delete from urlinfos where key = ?', [key])
        return 'success'
    except Exception, e:
        return e.message


@app.route('/votes/<int:key>', methods=['PUT'])
def url_put_vote_service(key):
    """
    vote add
    ---
    tags:
      - urls
    parameters:
      - name: key
        in: path
        required: true
        type: integer
    definitions:
      - schema:
          id: UrlInfo
          required:
            - key
            - title
            - url
            - description
            - vote
          properties:
                key:
                  type: integer
                  description: auto increment id
                title:
                  type: string
                  description: title of url
                url:
                  type: string
                  description: http url
                description:
                  type: string
                  description: describe the url
                vote:
                  type: integer
                  description: counter of clicking
    responses:
      200:
        description: Returns one url info
        schema:
            $ref: '#/definitions/UrlInfo'
    """

    try:
        update_db('update urlinfos set vote = vote + 1 where key = ?', [key])

        info = query_db('select * from urlinfos where key = ?', [key], one=True)
        if info is None:
            flash('no such urlinfo')
        else:
            url = {}
            url['key'] = int(info[0])
            url['title'] = info[1]
            url['url'] = info[2]
            url['description'] = info[3]
            url['vote'] = int(info[4])
        return jsonify(url)
    except Exception, e:
        return e.message


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.cli.command()
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    try:
        cur = g.db.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    except Exception, e:
        raise e.message


def delete_db(delete, args=(), one=False):
    try:
        res = g.db.execute(delete, args)
        if res is None:
            flash('fail to delete')
        g.db.commit()
    except Exception, e:
        raise e.message


def update_db(update, args=(), one=False):
    try:
        res = g.db.execute(update, args)
        if res is None:
            flash('fail to update')
        g.db.commit()
    except Exception, e:
        raise e.message


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0.0"
    swag['info']['title'] = "Swagger Monkey API"
    return jsonify(swag)

if __name__ == '__main__':
    #init_db()
    app.secret_key = "super secret key"
    app.run(host='0.0.0.0')
