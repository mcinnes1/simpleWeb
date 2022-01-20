from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from forms import LoginForm, PostForm, UserForm, PasswordForm, NameForm, SearchForm
from flask_ckeditor import CKEditor

#  JSON Example

# #  JSON 
# @app.route('/date')
# def get_current_date():
#     return {"Date": date.today()}


# Create a Flask instance
app = Flask(__name__)

# Add CKEditor
ckeditor = CKEditor(app)

#app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:11aa998Hjjj343434???@localhost/our_users'
app.config['SECRET_KEY'] = "itsasecret"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Flask login requirements

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))



# Search function

@app.route('/search', methods=["POST"])
def search():
	form = SearchForm()
	posts = Posts.query
	if form.validate_on_submit():
		# Get data from submitted form
		post.searched = form.searched.data
		# Query the database
		posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
		posts = posts.order_by(Posts.title).all()
		return render_template('search.html', form=form, searched=post.searched, posts=posts)

# pass to Navbar
@app.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)


# Create Admin page
@app.route('/admin')
@login_required
def admin():
	id = current_user.id
	if id == 21:
		return render_template('admin.html')
	else:
		flash("Sorry, Admin access only")
		return redirect(url_for('dashboard'))


# Login page

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("You are now logged in")
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong password, please try again")
		else:
			flash("User doesn't exist, please try again")

	return render_template('login.html', form=form)



# Logout Page

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You have logged out")
	return redirect(url_for('login'))



# Dashboard Page

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	form = UserForm()
	id = current_user.id
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']# same as validate_on_submit()
		name_to_update.email = request.form['email']
		name_to_update.hobby = request.form['hobby']
		name_to_update.username = request.form['username']
		name_to_update.about_author = request.form['about_author']

		try:
			db.session.commit()
			flash('User update success!')
			return render_template('dashboard.html',form=form, name_to_update=name_to_update)
		except:
			flash('Error, try again!')
			return render_template('dashboard.html',form=form, name_to_update=name_to_update)
	else:
		return render_template('dashboard.html',form=form, name_to_update=name_to_update,id=id)
	return render_template('dashboard.html')



# Delete individual post


@app.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
	post_to_delete = Posts.query.get_or_404(id)
	id = current_user.id
	if id == post_to_delete.poster.id:


		try:
			db.session.delete(post_to_delete)
			db.session.commit()
			flash("Post was deleted")
			posts = Posts.query.order_by(Posts.date_posted)
			return render_template("posts.html", posts=posts)
		except:
			flash("Error, Post not deleted")
			posts = Posts.query.order_by(Posts.date_posted)
			return render_template("posts.html", posts=posts)

	else:
			flash("Sorry, you cannot delete other users posts")
			posts = Posts.query.order_by(Posts.date_posted)
			return render_template("posts.html", posts=posts)



# Grab Posts from database

@app.route('/posts')
def posts():
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template("posts.html", posts=posts)



# Individual posts using id

@app.route('/posts/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html', post=post)



# Edit individual post

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		#post.author = form.author.data
		post.slug = form.slug.data
		post.content = form.content.data
		db.session.add(post)
		db.session.commit()
		flash("Post Has Been Updated!")
		return redirect(url_for('post', id=post.id))
	
	if current_user.id == post.poster_id:
		form.title.data = post.title
		#form.author.data = post.author
		form.slug.data = post.slug
		form.content.data = post.content
		return render_template('edit_post.html', form=form)
	else:
		flash("You Aren't Authorized To Edit This Post...")
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts)



# Add a post page

@app.route('/add-post', methods=['GET', 'POST'])
#@login_required
def add_post():
	form = PostForm()

	if form.validate_on_submit():
		poster = current_user.id
		post = Posts(title=form.title.data, content=form.content.data, poster_id=poster, slug=form.slug.data)
		form.title.data = ''
		form.content.data = ''
		#form.author.data = ''
		form.slug.data = ''
		db.session.add(post)
		db.session.commit()
		flash("Post submitted successfully")
	return render_template("add_post.html", form=form)



# Delete a user

@app.route('/delete/<int:id>')
def delete(id):
	user_to_delete = Users.query.get_or_404(id)
	name = None
	form = UserForm()

	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User deleted Successfully")
		our_users = Users.query.order_by(Users.date_added)
		return render_template('add_user.html', form=form, name=name,our_users=our_users)

	except:
		flash("Error, there was a problem, try again.")
		return render_template('add_user.html', form=form, name=name,our_users=our_users)



# Update existing record

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']# does same as validate_on_submit()
		name_to_update.email = request.form['email']
		name_to_update.hobby = request.form['hobby']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash('User update success!')
			return render_template('update.html',form=form, name_to_update=name_to_update)
		except:
			flash('Error, try again!')
			return render_template('update.html',form=form, name_to_update=name_to_update)
	else:
		return render_template('update.html',form=form, name_to_update=name_to_update, id=id)



# Add a user

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
			user = Users(username=form.username.data, name=form.name.data, email=form.email.data, hobby=form.hobby.data, password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.username.data = ''
		form.email.data = ''
		form.hobby.data  = ''
		form.password_hash.data = ''
		flash('User Submitted Successfully')
	our_users = Users.query.order_by(Users.date_added)
	return render_template('add_user.html', form=form, name=name,our_users=our_users)



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


@app.route('/name', methods=['GET','POST'])
def name():
	name = None
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
		flash('Submitted Successfully')
	return render_template('name.html', name=name, form=form)


@app.route('/test_pw', methods=['GET','POST'])
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None
	form = PasswordForm()

	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data
		form.email.data = ''
		form.password_hash.data = ''

		# Look up user by email
		pw_to_check = Users.query.filter_by(email=email).first()

		# Check hashed password
		passed = check_password_hash(pw_to_check.password_hash, password) # True or false

	return render_template('test_pw.html', email=email, password=password, 
			pw_to_check=pw_to_check, passed=passed, form=form)



class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(150))
	content = db.Column(db.Text)
	#author = db.Column(db.String(50))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(40), nullable=False)
	email = db.Column(db.String(50), nullable=False, unique=True)
	hobby = db.Column(db.String(50))
	about_author = db.Column(db.Text(400), nullable=True)
	profile_pic = db.Column(db.String(250), nullable=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	password_hash = db.Column(db.String(120))
	posts = db.relationship('Posts', backref='poster')

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute!')
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
 
	def __repr__(self):
		return '<Name %r>' % self.name

