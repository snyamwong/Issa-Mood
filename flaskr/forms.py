from wtforms import Form, StringField, SelectField
 
class SongSearch(Form):
    choices = [('Artist', 'Artist'),
               ('Song Name & Artist', 'Song Name & Artist')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')
