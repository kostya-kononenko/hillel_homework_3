import os
from flask import (Flask, render_template)

from flaskr.db import get_db


def create_app(test_config=None):
    # create and configure the app
    flask_hw = Flask(__name__, instance_relative_config=True)
    flask_hw.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(flask_hw.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        flask_hw.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        flask_hw.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(flask_hw.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @flask_hw.route("/")
    def head():
        return "Hello world!!!"

    @flask_hw.route('/names/')
    def names():
        db = get_db()
        names = db.execute(
            'SELECT COUNT(DISTINCT artist)'
            ' FROM track'
                ).fetchall()
        return render_template('names.html', names=names)

    @flask_hw.route('/tracks/')
    def traks():
        db = get_db()
        traks = db.execute(
            'SELECT COUNT(*)'
            ' FROM track'
        ).fetchone()
        return render_template('tracks.html', traks=traks)

    @flask_hw.route('/tracks/<genre_1>')
    def genre(genre_1):
        db = get_db()
        result = db.execute(
            "SELECT COUNT (*) FROM track WHERE genre = ?",
            (genre_1,)
        ).fetchall()[0]
        return render_template('genre.html', result=result, genre_1=genre_1)

    @flask_hw.route('/tracks-sec/')
    def tracks_sec():
        tracks = []
        db = get_db()
        result = db.execute(
            "SELECT title, track_length FROM track"
            ).fetchall()
        for row in result:
            tracks.append(row[0:len(row)])
        return render_template('track_length.html', result=tracks)

    @flask_hw.route('/tracks-sec/statistics/')
    def statistics():
        db = get_db()
        result = db.execute(
            "SELECT AVG(track_length) FROM track"
            ).fetchone()[0]
        total_duration = db.execute(
            "SELECT SUM(track_length) FROM track"
            ).fetchone()[0]
        return render_template('statistics.html', result=result, total_duration=total_duration)

    from . import db
    db.init_app(flask_hw)

    return flask_hw
