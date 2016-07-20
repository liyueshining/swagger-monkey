from contextlib import closing
from flask import Flask, g, jsonify, flash
from flask import request
from flask_cors import CORS, cross_origin
import sqlite3

DATABASE = 'swagger.db'
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)


@app.route('/urls', methods=['GET'])
def urls_get_service():
    try:
        urls = []
        infos = query_db('select * from urlinfos order by key')
        for info in infos:
            url = {}
            url['key'] = info[0]
            url['title'] = info[1]
            url['url'] = info[2]
            url['description'] = info[3]
            url['vote'] = info[4]
            urls.append(url)
        return jsonify(urls)
    except Exception as e:
        flash(e.message)
        return False


@app.route('/urls', methods=['POST'])
def urls_post_service():
    try:
        update_db('insert into urlinfos (title, url, description) values (?, ?, ?)',
              [request.json['title'], request.json['url'], request.json['description']])
        return 'success'
    except Exception as e:
        flash(e.message)
        return False

@app.route('/urls', methods=['DELETE'])
def urls_delete_service():
    try:
        delete_db('delete from urlinfos')
        return 'success'
    except Exception as e:
        flash(e.args)
        return False

@app.route('/url/<int:key>', methods=['GET'])
def url_get_service(key):
    try:
        info = query_db('select * from urlinfos where key = ?', [key], one=True)
        url = {}
        url['key'] = info[0]
        url['title'] = info[1]
        url['url'] = info[2]
        url['description'] = info[3]
        url['vote'] = info[4]

        return jsonify(url)
    except Exception as e:
        flash(e.args)
        return False

@app.route('/url/<int:key>', methods=['PUT'])
def url_put_service(key):
    try:
        update_db('update urlinfos set title=?, url=?, description=?, vote=? where key = ?',
              [request.json['title'], request.json['url'], request.json['description'],
               request.json['vote'], key])
        return 'success'
    except Exception as e:
        flash(e.args)
        return False

@app.route('/url/<int:key>', methods=['DELETE'])
def url_delete_service(key):
    try:
        delete_db('delete from urlinfos where key = ?', [key])
        return 'success'
    except Exception:
        return False

@app.route('/votes/<int:key>', methods=['PUT'])
def url_put_vote_service(key):
    try:
        update_db('update urlinfos set vote = title + 1 where key = ?', [key])
        return 'success'
    except Exception:
        return False


def update_db(update, args):
    try:
        res = g.db.execute(update, args)
        if res is None:
            flash('fail to update')
        g.db.commit()
        return res
    except Exception as e:
        raise e


def delete_db(delete, args):
    try:
        res = g.db.execute(delete, args)
        if res is None:
            flash('fail to delete')
        g.db.commit()
        return res
    except Exception as e:
        raise e


def query_db(query, args=(), one=False):
    try:
        cur = g.db.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        raise e


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def connect_db():
    """Connects to the specific database."""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.run()