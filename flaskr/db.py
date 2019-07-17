import psycopg2
import sys
import pickle
# Connect to an existing database


class Database:

    song_stored = False

    def data_exists(self, song_name, artist_name):

        # Open a cursor to perform database operations
        conn = psycopg2.connect(
            host="localhost",
            dbname="issamood",
            user="postgres",
            password="issamood",
        )
        cur = conn.cursor()

        # Execute a command: this creates a new table
        cur.execute("CREATE TABLE IF NOT EXISTS song_info (song_name varchar,artist_name varchar,album_img varchar,lyrics varchar,emotions BYTEA,agg_emotions BYTEA);")
        conn.commit()

        # Query the database and obtain data as Python objects
        cur.execute("SELECT song_name FROM song_info;")
        # gets all the query data
        data = cur.fetchall()
        # if data exists from query, search through it and compare song_name and artist_name and return true if its in the db
        if data:
            for data in data:
                if data[0] == song_name:
                    # print(data,file=sys.stderr)
                    cur.execute(
                        "SELECT artist_name FROM song_info WHERE song_name='{}';".format(song_name))
                    data = cur.fetchall()
                    for data in data:
                        if data[0] == artist_name:
                            self.song_stored = True
                            return self.song_stored
            # otherwise not in database return false
            return self.song_stored
        else:
            return self.song_stored

    def store_data(self, song_name, artist_name, album_img, lyrics, emotions, agg_emotions):

        conn = psycopg2.connect(
            host="localhost",
            dbname="issamood",
            user="postgres",
            password="issamood",
        )
        cur = conn.cursor()
        emotions = pickle.dumps(emotions)
        agg_emotions = pickle.dumps(agg_emotions)

        # if song isn't stored, insert data into database
        if self.song_stored == False:
            cur.execute("INSERT INTO song_info (song_name,artist_name,album_img,lyrics,emotions,agg_emotions) VALUES (%s,%s,%s,%s,%s,%s)",
                        (song_name, artist_name, album_img, lyrics, psycopg2.Binary(emotions), psycopg2.Binary(agg_emotions)))

        # Make the changes to the database persistent
        conn.commit()

        # Close communication with the database
        cur.close()
        conn.close()

    def retrieve_data(self, song_name, artist_name):
        conn = psycopg2.connect(
            host="localhost",
            dbname="issamood",
            user="postgres",
            password="issamood",
        )
        cur = conn.cursor()
        # get all data given song and artist
        cur.execute(
            "SELECT * FROM song_info WHERE song_name='{}' AND artist_name='{}';".format(song_name, artist_name))
        # store the query in data
        data = cur.fetchone()
        return data

        # Make the changes to the database persistent
        conn.commit()

        # Close communication with the database
        cur.close()
        conn.close()
