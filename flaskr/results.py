import sys
from lyrics import Lyrics
from genius import Genius
from db import Database
import pickle

def generate_results_data(song_string,artist_string,genius,results):
	lyrics = Lyrics()
	database = Database()
	
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

	results_data = [results,song_string,artist_string,album_img_string,emotions,agg_emotions]
	return results_data


def highlight_emotion_sentences(emotions_list, lyrics):
    highlight_line = False
    # list of emotions that will be iterated through
    emotion = ["anticipation", "joy", "trust", "sadness",
               "fear", "surprise", "anger", "disgust"]
    # 8 versions of the lyrics will be stored in this, all marked up for their respective emotion
    lyrics_list = []
    lyrics_temp = lyrics
    # run the loop once for each emotion
    for emotion in emotion:
        # for each clump of data, look at the emotions in the counter and see if it is present for that clump, if it is, set this line to be highlighted
        for clump in emotions_list:
            for counter in clump:
                if emotion in counter:
                    highlight_line = True

            if highlight_line == True:
                # sets the clumps current line of the song to be highlighted
                string_to_highlight = clump.original
                # if the mark for this string isn't a duplicate, add mark tags to that line of the song
                if lyrics_temp.find("<mark>{}</mark>".format(string_to_highlight)) == -1:
                    lyrics_temp = lyrics_temp.replace(
                        string_to_highlight, "<mark>{}</mark>".format(string_to_highlight))
                # reset back to false for the next iteration of the loop
                highlight_line = False

        # after it is done adding marks, add to the list
        lyrics_list.append(lyrics_temp)
        # reset the lyrics for the next emotion to have marks added to it
        lyrics_temp = lyrics

    # return lyrics marked up for all 8 emotions
    return lyrics_list
