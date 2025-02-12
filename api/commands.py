from flask.cli import with_appcontext
import click
from werkzeug.security import generate_password_hash

from .utils import db
from .models.users import User

@click.command("init_db")
@with_appcontext
def init_db():
    click.echo("Creating Database")
    db.drop_all()
    db.create_all()
    click.echo("Database Created")

@click.command("populate_db")
@with_appcontext
def populate_db():
    click.echo("Creating New Admin User")
    admin = User(username='01124096118',
                 name='Luka',
                 last_name='Varsimashvili',
                 email='varsimashvili.official@gmail.com',
                 phone_number='592159199',
                 password_hash=generate_password_hash('LUKAluka123'),
                 status=0,
                 is_admin=True)
    admin.create()
    click.echo("New Admin User Created")

