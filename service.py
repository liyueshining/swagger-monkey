from flask import Flask, g, jsonify, flash
from flask import request
import sqlite3
from entity.UrlInfo import UrlInfo

DATABASE = 'urlInfo.db'
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/urls', methods=['GET'])
def urls_get_service():
    urls = []
    infos = query_db('select * from urlinfos')
    for info in infos:
        url = {}
        url['key'] = info['key']
        url['title'] = info['title']
        url['url'] = info['url']
        url['description'] = info['description']
        url['vote'] = info['vote']
        urls.append(url)
    return jsonify({'UrlInfo': urls})


@app.route('/urls', methods=['POST'])
def urls_post_service():
     return update_db('insert into urlinfos ( title, url, description) values (?, ?, ?)', [request.json['title'], request.json['url'], request.json['description']])


@app.route('/urls', methods=['DELETE'])
def urls_delete_service():
    return delete_db('delete from urlinfos')


@app.route('/url/{key}', methods=['GET'])
def url_get_service(key):
    info = query_db('select * from urlinfos where key = ?', [key], one=True)
    url = {}
    url['key'] = info['key']
    url['title'] = info['title']
    url['url'] = info['url']
    url['description'] = info['description']
    url['vote'] = info['vote']
    return jsonify({'UrlInfo': url})



@app.route('/url/{key}', methods=['PUT'])
def url_put_service(key):
    return update_db('update urlinfos set title=?, url=?, description=? where key = ?', [request.json['title'], request.json['url'], request.json['description'], key], one=True)


@app.route('/url/{key}', methods=['DELETE'])
def url_delete_service(key):
    return delete_db('delete from urlinfos where key = ?', [key], one=True)


def update_db(update, args, one=False):
    cur = get_db().execute(update, args)
    if cur is None:
        flash('fail to update')
    return True


def delete_db(delete, args, one=False):
    cur = get_db().execute(delete, args)
    if cur is None:
        flash('fail to delete')
    return True


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.before_request
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')