from wtforms import Form, StringField, SelectField
 
class Song_search(Form):
    choices = [('Song Name', 'Song Name'),
               ('Song Name & Artist', 'Song Name & Artist')]
    select = SelectField('Search By:', choices=choices)
    song_string = StringField(u'Song Name')
    artist_string = StringField(u'Artist Name')
