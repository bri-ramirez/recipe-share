from datetime import datetime
from flask_app import app
from flask import flash, render_template, request, session, redirect

from flask_app.controllers.home import isLogged
from flask_app.models.recipe import Recipe

@app.route("/recipes")
def recipes():
    if not isLogged():
        return redirect("/")

    recipes = Recipe.getWithUsers()

    for recipe in recipes:
        print("USER: ",  recipe.user )


    return render_template("recipes/dashboard.html", recipes=recipes)

@app.route("/recipes/new")
def formCreateRecipe():
    if not isLogged():
        return redirect("/")

    # enviamos una receta vacía para evitar problemas en el formulario
    recipe = Recipe 
    return render_template("recipes/form.html", action="/recipes/new", recipe=recipe)


@app.route("/recipes/new", methods = ["POST"])
def createRecipe():
    if not isLogged():
        return redirect("/")

    if not Recipe.isValid(request.form):
        return redirect('/')

    under = 0
    if 'under' in request.form:
        under = 1
    
    data = {
        'name': request.form['name'],
        'desc': request.form['description'],
        'inst': request.form['instructions'],
        'datem': request.form['date_made'],
        'under': under,
        'user_id': session['user']['id']
    }

    recipeId = Recipe.save(data)

    if recipeId == False:
        flash('Lo sentimos, ha ocurrido un error al crear la receta!', 'warning')
        recipe = Recipe({
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'under': request.form['under'],
            'date_made': request.form['date_made'],
            'user_id': session['user']['id']
        })
        return render_template("/recipes/form.html", recipe=recipe)

    flash('has creado una receta correctamente!', 'success')
    return redirect('/recipes')


@app.route("/recipes/<int:recipe_id>")
def viewRecipe(recipe_id):
    recipe = Recipe.getOneWithUser(recipe_id)
    if recipe is False:
        flash("Lo sentimos, no se ha encontrado la receta", 'warning')
        redirect('/recipes')

    date = str(recipe.date_made).split(" ")
    recipe.date_made = date[0]

    return render_template('recipes/view.html', recipe=recipe)

@app.route("/recipes/edit/<int:recipe_id>")
def formEditRecipe(recipe_id):
    recipe = Recipe.get_one(recipe_id)

    if recipe is False:
        flash("Lo sentimos, no se ha encontrado la receta", 'warning')
        redirect('/recipes')

    date = str(recipe.date_made).split(" ")
    recipe.date_made = date[0]

    return render_template('recipes/form.html', recipe=recipe, action="/recipes/update")

@app.route("/recipes/update", methods=["POST"])
def updateRecipe():

    if not isLogged():
        return redirect("/")

    recipeId = request.form['recipe_id'];
    if not Recipe.isValid(request.form):
        flash('Lo sentimos, ha ocurrido un error al editar la receta!', 'danger')
        return redirect("/recipes/edit/" + str(recipeId))

    recipe = Recipe.get_one(recipeId)

    under = 0
    if 'under' in request.form:
        under = 1

    data = {
        'id': recipeId,
        'name': request.form['name'],
        'desc': request.form['description'],
        'inst': request.form['instructions'],
        'datem': request.form['date_made'],
        'under': under,
    }

    result = recipe.update(data)

    if result == False:
        flash('Lo sentimos, ha ocurrido un error al editar la receta!', 'danger')
        return redirect("/recipes/edit/" + str(recipeId))

    flash('Se ha editado la receta correctamente', 'success')
    return redirect('/recipes')

@app.route("/recipes/delete/<int:recipe_id>")
def deleteRecipe(recipe_id):
    if not isLogged():
        return redirect("/")

    recipe = Recipe.get_one(recipe_id)

    if recipe is False:
        flash("Lo sentimos, no se ha encontrado la receta", 'warning')
        redirect('/recipes')

    Recipe.delete_one(recipe_id)

    return redirect('/recipes')
