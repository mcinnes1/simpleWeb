# ----------------- Create and run a Virtual Environment -----------------------

#   Using Gitbash
# $ cd /h/git/simpleweb
# $ python -m venv virt
# $ source virt/scripts/activate
# $ pip freeze
# $ pip install flask
# $ touch simpleweb.py
# $ export FLASK_ENV=development
# $ export FLASK_APP=simpleweb.py
# $ flask run

# ----------------- Migration in gitbash, adding a column ----------------------

# Add column details to code first
# While inside virtual environment
# $ pip install Flask-Migrate
# $ flask db migrate -m 'Initial Migration'
#    An 'Initial Migration'.py File is created within working directory
# $ flask db upgrade


# ---------------- Steps to initialize new GIT project repository -------------

$ git config --global user.name "Your Name"
$ git config --global user.email "you@youraddress.com"
$ git config --global push.default matching
$ git config --global alias.co checkout
$ git init


