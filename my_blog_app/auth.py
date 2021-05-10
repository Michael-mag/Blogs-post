import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from my_blog_app.db import get_db

#create a blueprint called auth
bp = Blueprint("auth",__name__,url_prefix="/auth")


#the register view page for registration
@bp.route("/register",methods=("GET","POST"))
def register():
    if request.method == "POST":
        #then get the variables from the post
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()

        #error handling
        error = None
        if not username:
            error = "Username required"
        elif not password:
            error = "Password required"
        elif db.execute(
            'SELECT id FROM users WHERE username = ?', (username,)
            ).fetchone() is not None:
            error = "User {} is already registered.".format(username)
        
        #if everything is fine, proceed
        if error is None:
            db.execute("INSERT INTO users (username, password) VALUES (?,?)",
                      (username,generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for("auth.login"))
        
        flash(error)
    
    return render_template("auth/register.html")


#now the view function for the login page
@bp.route("/loging",methods=("GET","POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        error = None

        #try to fetch the user
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = "Username not found"
        elif not check_password_hash(user["password"],password):
            error = "Incorrect password"
        
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        
        flash(error)
    
    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    """
        - This function runs before the view function no matter what url is requested.
        - It checks if user id is stored in the session and gets that user's data from the db
            and stores it in g.user which lasts for the duration of the request.
    """
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM users WHERE id = ?",(user_id,)
        ).fetchone()


@bp.route("/logout")
def logout():
    """
        - Removes the users from the session so that on subsequent requests the user is no longer available
    """
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)
    return wrapped_view