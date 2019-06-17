from wtforms import Form, StringField, SelectField
 
class SongSearch(Form):
    choices = [('Song Name', 'Song Name'),
               ('Song Name & Artist', 'Song Name & Artist')]
    select = SelectField('Search By:', choices=choices)
    songSearch = StringField(u'Song Name')
    artistSearch = StringField(u'Artist Name')
