from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	first_name = "Ian"
	stuff = "This is <strong>Bold</strong> Text"
	inst = ['Guitar', 'Whistle', 'Piano', 'Uke']
	return render_template('index.html', first_name=first_name, stuff=stuff, inst=inst)


@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500