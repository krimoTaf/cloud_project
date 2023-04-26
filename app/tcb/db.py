import psycopg2
from psycopg2 import extras

import click
from flask import current_app, g

from tcb.fake_data import genrate_fake_data


# configure database connection
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=current_app.config['HOST'],
            database=current_app.config['DATABASE'],
            user=current_app.config['USER'],
            password=current_app.config['PASSWORD'],
            cursor_factory = extras.RealDictCursor
        )

    return g.db


# close and delete db from contexte
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Initialize database
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        with db:
            with db.cursor() as curs:
                curs.execute(f.read().decode('utf8'))

    # add some fake data to our database           
    genrate_fake_data(db)
    


# create commande with click package to use it in terminale
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Database initialization...')


# add our close db and new command init_db_command to application context
# teardown_appcontext call close_db when flask application when context is pop
# app.cli.add_command add init-db command to flask application 
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)