# Issa-Mood

## pip list

pip install -r requirements

## Lexicon

The Lexicon used for this project is located here

https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm

## Foundation

https://zurb.com/playground/foundation-icon-fonts-3#customize

https://foundation.zurb.com/

Download the files, and move them into static/css directory.

## Setting up Postgre

Download pgadmin/postgre

Once you download pgadmin, set up a super user

Go into Servers -> Databases -> and create new database named issamood with user named "postgres" and pw "issamood"

In order to see all data in the tables go into Schemas -> Tables -> and then right click song_info table and click View/Edit Data

## Running Instructions

Install Python 3.7.3

verify installation with "python --version"

Make sure you run the above pip command (also make you sure update the requirements.txt whenever you install a new package!)

Make sure you have the lexicon installed.

Make sure you have foundation installed.

clone project with "git clone $URL"

Move into git directory

Run the command ". run.sh"

Go to http://127.0.0.1:5000/home to verify that the web app is working correctly
