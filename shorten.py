from flask import Flask
from flask import render_template

from url_shortener import url_generator
from url_shortener import url_fetcher

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('cover.html')

@app.route('/shorten/', methods=['GET'])
def shorten():
	if request.method == 'GET':
		url = request.args.get("full_url")

		if url is None:
			render_template('cover.html', error="yes")

		new_hash = url_generator(url)
		
		#return render_template('cover.html', hash=new_hash)
		print new_hash
	else:
		return render_template('cover.html', error="yes")

@app.route('/<url_hash>')
def fetch_and_redirect(url_hash):
	target_url = url_fetcher(url_hash)

	if target_url is False:
		return render_template('404.html')
	else:
		return redirect(target_url, code=302)