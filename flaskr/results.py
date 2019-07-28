"""
"""
import sys
import pickle
from lyrics import Lyrics
from db import Database


def generate_results_data(song_string, artist_string, genius, results):
    """
    """

    lyrics = Lyrics()
    database = Database()

    song_string = genius.song
    artist_string = genius.artist
    # if data's song and artist doesn't exist in db, do normal loading and then store in db
    if not database.data_exists(song_string, artist_string):
        album_img_string = genius.album_img
        #time0 = time.time()
        filtered_lyrics = lyrics.filter_lyrics(results)
        emotions = lyrics.get_lyrics_emotions(filtered_lyrics)
        agg_emotions = lyrics.get_agg_emotions(filtered_lyrics)
        # takes in all of the info that is passed to the template and stores it for later use
        database.store_data(song_string, artist_string,
                            album_img_string, results, emotions, agg_emotions)
    # if data exists in database, retrieve it and then store it's normal variables
    else:
        database_data = database.retrieve_data(song_string, artist_string)
        album_img_string = database_data[2]
        results = database_data[3]
        emotions = pickle.loads(database_data[4])
        agg_emotions = pickle.loads(database_data[5])

    results = highlight_emotion_sentences(emotions, results)

    results_data = [results, song_string, artist_string,
                    album_img_string, emotions, agg_emotions]

    return results_data


def highlight_emotion_sentences(emotions_list, lyrics):
    """
    """

    # list of emotions that will be iterated through
    emotions = {"anticipation": "#FF7F00",
                "joy": "#FFEA52",
                "trust": "#52FF52",
                "sadness": "#0000CA",
                "fear": "#009800",
                "surprise": "#008BE2",
                "anger": "#D60000",
                "disgust": "#E000E0"}

    # 8 versions of the lyrics will be stored in this, all marked up for their respective emotion
    lyrics_list = []
    lyrics_temp = lyrics
    highlight_line = False

    # run the loop once for each emotion
    for emotion, color in emotions.items():
        # for each clump of data, look at emotions in counter
        # if it is present for that clump set this line to be highlighted
        for clump in emotions_list:
            for counter in clump:
                if emotion in counter:
                    highlight_line = True

            if highlight_line:
                # sets the clumps current line of the song to be highlighted
                string_to_highlight = clump.original
                # if the mark for this string isn't a duplicate, add mark tags to that line
                if lyrics_temp.find("<mark>{}</mark>".format(string_to_highlight)) == -1:
                    if emotion in ["anticipation", "sadness", "fear", "anger", "disgust"]:
                        mark_style = "style=\"background-color: {}; color: white\"".format(
                            color)
                    else:
                        mark_style = "style=\"background-color: {}\"".format(
                            color)

                    mark_tag = "<mark {}>{}</mark>".format(
                        mark_style, string_to_highlight)

                    print(mark_tag, file=sys.stderr)

                    lyrics_temp = lyrics_temp.replace(
                        string_to_highlight, mark_tag)

                    # reset back to false for the next iteration of the loop
                    highlight_line = False

        # after it is done adding marks, add to the list
        lyrics_list.append(lyrics_temp)
        # reset the lyrics for the next emotion to have marks added to it
        lyrics_temp = lyrics

    # return lyrics marked up for all 8 emotions
    return lyrics_list
