from flask_app import app
from flask import flash, session, redirect, request
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/register", methods = ["POST"])
def createUser():
    if not User.validUser(request.form):
        return redirect('/')

    pwHash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'fname': request.form['first_name'],
        'lname': request.form['last_name'],
        'email': request.form['email'],
        'password': pwHash
    }
    userId = User.save(data)

    if userId is False:
        flash("Error al registrar usuario", "danger")
        return redirect('/')

    session['user'] = {
        'id': userId,
        'name': data["fname"] +" "+ data["lname"],
    }

    return redirect('/recipes')

@app.route("/login", methods = ["POST"])
def loginUser():
    user = User.getByEmail(request.form['email'])

    if user is False:
        flash('email / password incorrectos!', 'warning')
        return redirect('/')

    print("PSW", bcrypt.check_password_hash(user.password, request.form['password']))
    if bcrypt.check_password_hash(user.password, request.form['password']) == False:
        flash('email / password incorrectos!', 'warning')
        return redirect('/')

    session['user'] = {
        'id': user.id,
        'name': user.first_name +" "+ user.last_name
    }

    print(session["user"])
    return redirect('/recipes')