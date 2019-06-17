import os
import sys
from flask import Flask, flash, render_template, request, redirect
from forms import SongSearch
from genius import GetLyrics



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/home', methods=['GET','POST'])
    def home():
        search = SongSearch(request.form)
        if request.method == 'POST':
            return search_results(search)

        return render_template('home.html', form=search)

    @app.route('/results')
    def search_results(search):
        search_type = search.data['select']
        song_string = search.data['songSearch']
        artist_string = ""
        if search_type == "Song Name & Artist":
            artist_string = search.data['artistSearch']

       # print(search_type, file=sys.stderr)
        results = GetLyrics(song_string,artist_string)
        if results != None:
            artist_string = GetLyrics.artist
            return render_template('results.html', lyrics=GetLyrics(song_string,artist_string),songTitle=song_string,artistName=artist_string)
        else:
            flash('No results found!')
            return redirect('/home')

    @app.route('/graphs')
    def graphs():
        return render_template('graphs.html')

    return app