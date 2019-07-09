import requests
import types
from bs4 import BeautifulSoup

class Genius:
  base_url = "https://api.genius.com"
  #this is the authorization token unique to the genius account to make API calls
  headers = {'Authorization': 'Bearer 9mtf9FXSDPyq-UH7wBY_opdVHOtxCgIY1yfME3OEfRoPFbTSuw5hmxjPh0kEpc5h'}
  artist = None
  song = None
  album_img = None

  def lyrics_from_song_api_path(self,song_api_path):
    #path for the song genius API selected
    song_url = self.base_url + song_api_path
    response = requests.get(song_url, headers=self.headers)
    json = response.json()
    path = json["response"]["song"]["path"]

    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    #bs4 call to get the html of the page
    html = BeautifulSoup(page.text, "html.parser")
    #parses the lyrics and then returns it
    [h.extract() for h in html('script')]
    lyrics = html.find("div", class_="lyrics").get_text()
    return lyrics

  def get_lyrics(self,song_title,artist_name):
    song_title = song_title
    artist_name = artist_name
    search_url = self.base_url + "/search"
    data = {'q': song_title}
    #makes an API call to genius given the base url,song title, auth token
    response = requests.get(search_url, data=data, headers=self.headers)
    json = response.json()
    #this var is None until the parsing finds a suitable result
    song_info = None
    #if no artist name given, assign the first artist name in hits found to artist_name
    if artist_name == "":
      for hit in json["response"]["hits"]:
        artist_name = hit["result"]["primary_artist"]["name"]
        break
    #parse through hits until the artist_name is the same as the hits stored artist name
    for hit in json["response"]["hits"]:
      if hit["result"]["primary_artist"]["name"] == artist_name:
        #stores method variable to be sent later to results page
        self.artist = artist_name
        self.song = hit["result"]["title"]
        self.album_img = hit["result"]["header_image_thumbnail_url"]
        song_info = hit
        break
    #if theres a hit stored, get the path and call method to web scrape lyrics
    if song_info:
      song_api_path = song_info["result"]["api_path"]
      return self.lyrics_from_song_api_path(song_api_path)

