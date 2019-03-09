import os
import click

from flask import Flask
from bluelog.extensions import db
from bluelog.settings import config
from bluelog.models import Admin, Post, Category, Comment


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_commands(app)
    register_shell_context(app)

    return app


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            db=db, Admin=Admin,
            Post=Post, Category=Category,
            Comment=Comment)


def register_extensions(app):
    db.init_app(app)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initdb(drop):
        '''
        init database for websit.
        '''
        if drop:
            click.confirm('Drop database?!')
            db.drop_all()
            click.echo('Drop table')
        db.create_all()
        click.echo('Initialized database')

    @app.cli.command()
    @click.option('--category', default=10, help='Created category count')
    @click.option('--comment', default=500, help='Created comment count')
    @click.option('--post', default=50, help='Created post count')
    def forge(category, post, comment):
        '''
        Prepare fake data for testing.
        '''
        from bluelog.fakes import fake_admin, fake_categories,\
            fake_comments, fake_posts
        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)
        click.echo('Finish!')
