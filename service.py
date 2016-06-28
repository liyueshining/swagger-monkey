from contextlib import closing
from flask import Flask, g, jsonify, redirect, url_for, flash
from flask import request
import sqlite3

DATABASE = 'swagger.db'
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/urls', methods=['GET'])
def urls_get_service():
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
    return jsonify({'UrlInfo': urls})


@app.route('/urls', methods=['POST'])
def urls_post_service():
    update_db('insert into urlinfos (title, url, description) values (?, ?, ?)',
              [request.json['title'], request.json['url'], request.json['description']])
    return 'success'


@app.route('/urls', methods=['DELETE'])
def urls_delete_service():
    delete_db('delete from urlinfos')

    return 'success'


@app.route('/url/<int:key>', methods=['GET'])
def url_get_service(key):
    info = query_db('select * from urlinfos where key = ?', [key], one=True)

    url = {}
    url['key'] = info[0]
    url['title'] = info[1]
    url['url'] = info[2]
    url['description'] = info[3]
    url['vote'] = info[4]

    return jsonify({'UrlInfo': url})


@app.route('/url/<int:key>', methods=['PUT'])
def url_put_service(key):
    update_db('update urlinfos set title=?, url=?, description=?, vote=? where key = ?',
              [request.json['title'], request.json['url'], request.json['description'],
               request.json['vote'], key])
    return 'success'


@app.route('/url/<int:key>', methods=['DELETE'])
def url_delete_service(key):
    res = delete_db('delete from urlinfos where key = ?', [key])

    return 'success'


def update_db(update, args):
    res = g.db.execute(update, args)
    if res is None:
        flash('fail to update')
    g.db.commit()
    return res


def delete_db(delete, args):
    res = g.db.execute(delete, args)
    if res is None:
        flash('fail to delete')
    g.db.commit()
    return res


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


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