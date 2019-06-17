import requests
from bs4 import BeautifulSoup

base_url = "https://api.genius.com"
headers = {'Authorization': 'Bearer 9mtf9FXSDPyq-UH7wBY_opdVHOtxCgIY1yfME3OEfRoPFbTSuw5hmxjPh0kEpc5h'}

def lyrics_from_song_api_path(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]

  page_url = "http://genius.com" + path
  page = requests.get(page_url)
  html = BeautifulSoup(page.text, "html.parser")
 
  [h.extract() for h in html('script')]
  lyrics = html.find("div", class_="lyrics").get_text() 
  #lyrics.replace('\n', ' ')
  return lyrics

def GetLyrics(song_title,artist_name):
  song_title = song_title
  artist_name = artist_name

  search_url = base_url + "/search"
  data = {'q': song_title}
  response = requests.get(search_url, data=data, headers=headers)
  json = response.json()
  song_info = None
  if artist_name == "":
    for hit in json["response"]["hits"]:
      if hit["result"]["title"].lower()== song_title.lower():
        GetLyrics.artist = hit["result"]["primary_artist"]["name"]
        song_info = hit
      break
  else:
    for hit in json["response"]["hits"]:
      if hit["result"]["primary_artist"]["name"] == artist_name:
        GetLyrics.artist = artist_name
        song_info = hit
      break
  if song_info:
    song_api_path = song_info["result"]["api_path"]
    return lyrics_from_song_api_path(song_api_path)