from flask import Flask, render_template, request, make_response, redirect, url_for
from models import db, User

app = Flask(__name__)
db.create_all()

@app.route("/", methods=["GET"])
def index():
    all_users = db.query(User).all()
    return render_template("index.html", users=all_users)

@app.route("/delete", methods=["GET"])
def delete():
    user_id = request.args.get("id")
    if user_id:
        user = User.query.get(user_id)
        user.deleted = True
    return make_response(redirect(url_for('index')))


@app.route("/add_edit", methods=["GET", "POST"])
def add_edit():
    user = None
    user_id = request.args.get("id")
    if user_id:
        user = db.query(User).get(user_id)
    if request.method == "GET":  # show form
        return render_template("add_edit.html", user=user)
    else: # handle submission
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        if user: #update
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
        else: # create
            user = User(first_name=first_name, last_name=last_name, email=email)
        db.add(user)
        db.commit()
        return make_response(redirect(url_for('index')))

if __name__ == "__main__":
    app.run()
    
    
