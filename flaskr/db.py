import psycopg2
import sys
# Connect to an existing database

class Database:

	song_stored=False

	def data_exists(self,song_name,artist_name):

		# Open a cursor to perform database operations
		conn = psycopg2.connect(
			host="localhost",
			dbname="issamood",
		 	user="postgres",
		 	password="issamood",
		)
		cur = conn.cursor()

		# Execute a command: this creates a new table
		cur.execute("CREATE TABLE IF NOT EXISTS song_info (song_name varchar,artist_name varchar,album_img varchar,lyrics varchar,emotions text,agg_emotions text);")
		conn.commit()
		# Pass data to fill a query placeholders and let Psycopg perform

		# Query the database and obtain data as Python objects
		cur.execute("SELECT song_name FROM song_info;")
		data = cur.fetchall()
		if data:
			for data in data:
				if data[0]==song_name:
					#print(data,file=sys.stderr)
					cur.execute("SELECT artist_name FROM song_info WHERE song_name='{}';".format(song_name))
					data = cur.fetchall()
					for data in data:
						if data[0]==artist_name:
							self.song_stored=True
							return self.song_stored
			return False
		else:
			return False


	def store_data(self,song_name,artist_name,album_img,lyrics,emotions,agg_emotions):

		# Open a cursor to perform database operations
		conn = psycopg2.connect(
			host="localhost",
			dbname="issamood",
		 	user="postgres",
		 	password="issamood",
		)
		cur = conn.cursor()
		if self.song_stored == False:
			cur.execute("INSERT INTO song_info (song_name,artist_name,album_img,lyrics,emotions,agg_emotions) VALUES (%s,%s,%s,%s,%s,%s)",
			(song_name,artist_name,album_img,lyrics,str(emotions),str(agg_emotions)))

		# Make the changes to the database persistent
		conn.commit()

		# Close communication with the database
		cur.close()
		conn.close()

	def retrieve_data(self,song_name,artist_name):
		conn = psycopg2.connect(
			host="localhost",
			dbname="issamood",
		 	user="postgres",
		 	password="issamood",
		)
		cur = conn.cursor()

		cur.execute("SELECT * FROM song_info WHERE song_name='{}' AND artist_name='{}';".format(song_name,artist_name))
		data = cur.fetchone()
		return data

		# Make the changes to the database persistent
		conn.commit()

		# Close communication with the database
		cur.close()
		conn.close()