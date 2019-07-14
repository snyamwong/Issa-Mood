import os
import sys
import pickle
from lyrics import Lyrics
from flask import Flask, flash, render_template, request, redirect
from forms import Song_search
from genius import Genius
from db import Database
from results import highlight_emotion_sentences
import pickle
import time

def create_app(test_config=None):
    """
    """
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

    @app.route('/home', methods=['GET', 'POST'])
    def home():
        #Song_search is the form from forms.py where all the form data is stored
        search = Song_search(request.form)
        if request.method == 'POST':
            #this calls the results template and genius API from genius.py/GetLyrics
            return search_results(search)

        return render_template('home.html', form=search)

    @app.route('/results')
    def search_results(search):
        lyrics = Lyrics()
        genius = Genius()
        database = Database()
        #this is the stored value for dropdown either: Song Name or Song Name & Artist
        search_type = search.data['select']
        #Name of the song to search for
        song_string = search.data['song_string']
        artist_string = ""
        #If user is searching by Song & Artist, store a value in artist_string
        if search_type == "Song Name & Artist":
            artist_string = search.data['artist_string']
       # print(search_type, file=sys.stderr)

        #GetLyrics is the genius/bs4 call to get lyrics from genius.py
        results = genius.get_lyrics(song_string, artist_string)
        #if results exist, render the page and information, else flash on home page "no results"
        if results is not None:
            song_string = genius.song
            artist_string = genius.artist
            #if data's song and artist don't exist in the database, do all the normal heavy loading and then store it in the database
            if database.data_exists(song_string,artist_string)==False:
                album_img_string = genius.album_img
                #time0 = time.time()
                filtered_lyrics = lyrics.filter_lyrics(results)
                emotions = lyrics.get_lyrics_emotions(filtered_lyrics)
                agg_emotions = lyrics.get_agg_emotions(filtered_lyrics)
                #this takes in all of the information that is passed to the tenplate normally and stores it for later use
                database.store_data(song_string,artist_string,album_img_string,results,emotions,agg_emotions)
            #if data exists in database, retrieve it and then store it's normal variables
            else:
                database_data = database.retrieve_data(song_string,artist_string)
                album_img_string=database_data[2]
                results=database_data[3]
                emotions=pickle.loads(database_data[4])
                agg_emotions=pickle.loads(database_data[5])

            results = highlight_emotion_sentences(emotions,results)
            #time1 = time.time()
            #print(results, file=sys.stderr)
            #print(emotions, file=sys.stderr)
            #print(time1 - time0, file=sys.stderr)
            return render_template('results.html',
                                   lyrics=results,
                                   songTitle=song_string,
                                   artistName=artist_string,
                                   album_img=album_img_string,
                                   emotions=emotions,
                                   agg_emotions=agg_emotions)
        flash('No results found!')
        return redirect('/home')

    @app.route('/graphs')
    def graphs():
        return render_template('graphs.html')

    return app
