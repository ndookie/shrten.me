from flask import Flask, render_template, request, url_for, g, redirect, request
import sqlite3, sys, re
from base_converter import base_conversion, hash_to_number

app = Flask(__name__)

@app.before_request
def before_request():
	g.db = sqlite3.connect("static/shortener.db")

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()


# The base for encoding and decoding of the hashes.
base = 62

html_escape_table = [
     ("&", "&amp;"),
     ('"', "&quot;"),
     (">", "&gt;"),
     ("'", "&apos;"),
     ("<", "&lt;")
     ]


# Function for inserting new URL into database.
def insert_url(url):

	con = g.db
	cur = g.db.cursor()

	# Remove http(s):// from the links if they contain them.
	url = re.sub('^https?://', '', url)

	# Insert url into table with other fields left empty.
	cur.execute("INSERT INTO url_table VALUES(NULL,'%s',NULL, NULL)" % (url))

	# Fetch the generated ID from the table for the inserted URL.
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
	con = g.db
	cur = g.db.cursor()

	# Updates the table entry for the URL with the hash.
	user_ip = str(request.remote_addr)
	cur.execute("UPDATE url_table SET shortened_url='" + hash + "', ip='" + user_ip + "'  WHERE id=%i" % (id));
	con.commit()
	return

# Takes a url, inserts it into the database and returns the hash.
def url_generator(url):
	
	new_id = insert_url(url)
	shortened_url = generate_hash(new_id)
	update_shortened_url(new_id, shortened_url)

	return shortened_url

# Fetches corresponding URL for hash from database.
def url_fetcher(hash):
	
	fetching_id = hash_to_number(hash, base)
	con = g.db
	cur = g.db.cursor()

	cur.execute("SELECT url FROM url_table WHERE id=" + str(fetching_id))
	url = cur.fetchall()
	url = url[-1]

	if url[0] is None:
		return False
	else:
		return url[0]



#**********************ROUTES***********************#

@app.route('/')
def index():
	return render_template('main.html')

@app.route('/shorten/', methods=['GET'])
def shorten():
	if request.method == 'GET':
		unescaped_url = request.args.get("full_url")

		# Escaping unsavoury characters.
		url = map(lambda rule: unescaped_url.replace(rule[0], rule[1]), html_escape_table)[0]
		
		# This is here until I figure out wtf is going on.
		url = url.replace("'", "&apos;")

		if url is None:
			return render_template('main.html', error="yes")
			return

		new_hash = url_generator(url)
		
		return render_template('main.html', hash=new_hash)
	else:
		return render_template('main.html', error="yes")

@app.route('/<url_hash>')
def fetch_and_redirect(url_hash):

	target_url = url_fetcher(url_hash)

	if target_url is False:
		return render_template('404.html')
	else:
		return redirect("http://" + target_url)

if __name__ == '__main__':
	app.run(debug=True)

