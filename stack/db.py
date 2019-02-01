from google.cloud import datastore
from . import settings

def start_db():
    db = datastore.Client(project=settings.env.project_id)
    return db


def query_user(client, username):
    query = client.query(kind='Stack-user')
    query.add_filter('username', '=', username)
    return list(query.fetch())
    

def add_user(client, username, password):
    get_key = client.key('Stack-user')
    new_entity = datastore.Entity(get_key)
    new_entity.update({
        'username': username,
        'password': password
    })
    client.put(new_entity)

