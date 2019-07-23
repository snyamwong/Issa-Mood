import requests
import types
from bs4 import BeautifulSoup
import sys
from lyrics import Lyrics
import pickle
import psycopg2


class Obama_Speeches:
    base_url = "https://api.genius.com"
    # this is the authorization token unique to the genius account to make API calls
    headers = {
        'Authorization': 'Bearer 9mtf9FXSDPyq-UH7wBY_opdVHOtxCgIY1yfME3OEfRoPFbTSuw5hmxjPh0kEpc5h'}
   

    def lyrics_from_song_api_path(self, song_api_path):
        # path for the song genius API selected
        song_url = self.base_url + song_api_path
        response = requests.get(song_url, headers=self.headers)
        json = response.json()
        path = json["response"]["song"]["path"]

        page_url = "http://genius.com" + path
        page = requests.get(page_url)
        # bs4 call to get the html of the page
        html = BeautifulSoup(page.text, "html.parser")
        # parses the lyrics and then returns it
        [h.extract() for h in html('script')]
        lyrics = html.find("div", class_="lyrics").get_text()
        return lyrics

    def get_lyrics(self):
        years = ["2009","2010","2011","2012","2013","2014","2015","2016"]
        data_list = []
        for year in years:
            artist_name = "Barack Obama"
            search_url = self.base_url + "/search"
            data = {'q': "Barack Obama State of the union {}".format(year)}
            print("Barack Obama State of the union {}".format(year),file=sys.stderr)
            # makes an API call to genius given the base url,song title, auth token
            response = requests.get(search_url, data=data, headers=self.headers)
            json = response.json()
            # this var is None until the parsing finds a suitable result
            song_info = None
            # if no artist name given, assign the first artist name in hits found to artist_name
            for hit in json["response"]["hits"]:
                if hit["result"]["primary_artist"]["name"] == artist_name:
                    # stores method variable to be sent later to results page
                    artist = artist_name
                    song = hit["result"]["title"]
                    song_info = hit
            # if theres a hit stored, get the path and call method to web scrape lyrics
                    if song_info:
                        song_api_path = song_info["result"]["api_path"]
                        lyrics = self.lyrics_from_song_api_path(song_api_path)

                    data = [song,artist,lyrics]
                    data_list.append(data)
                    break
                    
        return data_list

def store_data(song_name, artist_name, lyrics, emotions, agg_emotions):

    conn = psycopg2.connect(
        host="localhost",
        dbname="issamood",
        user="postgres",
        password="issamood",
    )
    cur = conn.cursor()
    emotions = pickle.dumps(emotions)
    agg_emotions = pickle.dumps(agg_emotions)

    cur.execute("CREATE TABLE IF NOT EXISTS speeches_info (song_name varchar,artist_name varchar,lyrics varchar,emotions BYTEA,agg_emotions BYTEA);")
    conn.commit()


    # if song isn't stored, insert data into database
    cur.execute("INSERT INTO speeches_info (song_name,artist_name,lyrics,emotions,agg_emotions) VALUES (%s,%s,%s,%s,%s)",
                (song_name, artist_name, lyrics, psycopg2.Binary(emotions), psycopg2.Binary(agg_emotions)))

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

def main():
    obama_speeches = Obama_Speeches().get_lyrics()
    lyrics = Lyrics()
    for speeches in obama_speeches:
        filtered_lyrics = lyrics.filter_lyrics(speeches[2])
        emotions = lyrics.get_lyrics_emotions(filtered_lyrics)
        speeches.append(emotions)
        agg_emotions = lyrics.get_agg_emotions(filtered_lyrics)
        speeches.append(agg_emotions)
        store_data(speeches[0],speeches[1],speeches[2],speeches[3],speeches[4])

if __name__ =="__main__":
    main()

