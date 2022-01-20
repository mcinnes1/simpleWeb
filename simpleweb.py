from flask import Flask, render_template, url_for


# Create a Flask Instance
app = Flask(__name__)


@app.route('/')
def home():
	return render_template('home.html', title='Home')


@app.route('/user')
def user():
	return render_template('user.html', title='User')



# Custom Error Pages
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500