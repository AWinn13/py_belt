from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.loginandreg import User
from flask_app.models.shows import Show
from flask_app.models.likes import Like


# -------------Dashboard-------------------
@app.route("/shows")
def welcome_user():
    #!------Route Guard--------
    if "user_id" not in session:
        return redirect("/")
    user = User.get_id({"id": session["user_id"]})
    return render_template("welcome.html", user=user, all_shows = Show.get_all(), all_likes = Like.get_all() )


# ------------Display show--------
@app.route("/shows/<int:id>")
def display_show(id):
    if "user_id" not in session:
        return redirect("/")
    show = Show.get_one_show({"id": id})
    user = User.get_id({"id": session["user_id"]})
    # all_shows = show.get_all()
    return render_template("display_show.html", user=user, show=show )


# ------Render create template-------


@app.route("/shows/create")
def render_show():
    if "user_id" not in session:
        return redirect("/")
    return render_template("new_show.html")


# ------Submit New show--------


@app.route("/shows/create/new", methods=["post"])
def create_show():
    if "user_id" not in session:
        return redirect("/")
    if not Show.validate_show(request.form):
        return redirect("/shows/create")
    data = {**request.form, "user_id": session["user_id"]}
    Show.create_show(data)
    return redirect("/shows")



# -------Render Edit show-------


@app.route("/shows/<int:id>/edit")
def edit_show(id):
    if "user_id" not in session:
        return redirect("/")
    this_show = Show.get_one_show({"id": id})
    return render_template("edit_show.html", this_show=this_show)


# ----------Update show-----------------


@app.route("/shows/<int:id>/update", methods=["post"])
def update_show(id):
    if "user_id" not in session:
        return redirect("/")
    if not Show.validate_show(request.form):
        return redirect(f"/shows/{id}/edit")
    data = {**request.form, "user_id": session["user_id"], 'id':id}
    Show.update_show(data)
    return redirect("/shows")


# ---------Delete show--------
@app.route("/shows/<int:id>/delete")
def delete_show(id):
    if "user_id" not in session:
        return redirect("/")
    Show.delete_show({"id": id})
    return redirect("/shows")

@app.route("/shows/<int:id>/skeptic", methods=["post"])
def update_skeptic(id):
    if "user_id" not in session:
        return redirect("/")
    data = {**request.form, "user_id": session["user_id"], 'id':id}
    Show.update_skeptic(data)
    return redirect("/shows")

@app.route("/shows/<int:id>/delete_like")
def delete_like(id):
    if "user_id" not in session:
        return redirect("/")
    Like.delete_like({"user_id": session["user_id"],"id": id})
    return redirect("/shows")

@app.route("/shows/<int:id>/add_like")
def add_like(id):
    if "user_id" not in session:
        return redirect("/")
    Like.add_like({"user_id": session["user_id"],"id": id})
    return redirect("/shows")
