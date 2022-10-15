from flask_app import app
from flask import render_template, session, redirect

@app.route("/")
def index():
    if not isLogged():
        return render_template("login.html")
    return redirect('/recipes')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

# validamos que se encuentre una sesión activa
def isLogged():
    if 'user' in session:
        return True

    return False