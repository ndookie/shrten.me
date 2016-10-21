#!/bin/python

# Importing integer base converter.
from base_converter import base_conversion
from base_converter import hash_to_number

import sqlite3 as lite
import sys

base = 62

# Database set up
try:
	con = None
	con = lite.connect('shortener.db');
	cur = con.cursor()
except:
	print "Connection to database has failed."
	sys.exit()

# Function for inserting new URL into database.
def insert_url(url):
	cur.execute("INSERT INTO url_table VALUES(NULL,'%s',NULL)" % (url))

	cur.execute("SELECT id FROM url_table WHERE url='%s'" % (url));

	url_id = cur.fetchall()

	url_id = url_id[-1]

	return url_id[0]

# Generates hash based off id from table.
def generate_hash(id):
	new_hash = base_conversion(id,base)

	return new_hash

# Updates the entry for a specific ID with it's hash.
def update_shortened_url(id, hash):
	cur.execute("UPDATE url_table SET shortened_url='" + hash + "' WHERE id=%i" % (id));

	con.commit()
	return

# Fetches corresponding URL for hash from database.
def url_fetcher(hash):
	fetching_id = hash_to_number(hash, base)

	cur.execute("SELECT url FROM url_table WHERE id=" + str(fetching_id))
	url = cur.fetchall()
	url = url[-1]

	con.close()

	return url[0]


# Takes a url, inserts it into the database and returns the hash.
def url_generator(url):
	new_id = insert_url(url)
	shortened_url = generate_hash(new_id)
	update_shortened_url(new_id, shortened_url)

	con.close()

	return shortened_url

#hash_to_number("Fgn", 62)
#print base_conversion(123456, 62)

print url_fetcher("L")

#url_generator('nigelriazdookie.com')

