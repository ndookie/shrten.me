from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('cover.html')

@app.route('/shorten/', methods=['GET'])
def shorten():
	if request.method == 'GET':
		print "nigel"
	else:
		render_template('cover.html', error="yes")


