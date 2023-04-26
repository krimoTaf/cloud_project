import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from tcb.db import get_db
from tcb.upload_s3 import upload_S3
from tcb.download_avatar import download_avatar


bp = Blueprint('auth', __name__, url_prefix='/auth')



# register view function 
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']

        db = get_db()
        error = None

        if not username:
            error = "Le nom d'utilisateur est obligatoire."
        elif not password:
            error = "Le mot de passe est obligatoire."
        elif gender not in ("male", "female"):
            error = "Gender is required ! (binary choice please)"
        

        if error is None:
            try:
                # get user data from users table
                with db:
                    with db.cursor() as curs:
                        curs.execute("SELECT * FROM users WHERE username = %s", (username,))
                        user = curs.fetchone()

                avatar = ""
                if user is None:
                    avatar = download_avatar(gender, username)
                    upload_S3(avatar, "tcb-cloud", "avatar/"+avatar)
                
                with db:
                    with db.cursor() as curs:
			            # url of our bucket
                        S3_url = current_app.config['AWS_S3_LINK']
                        curs.execute("INSERT INTO users (username, password, gender, avatar) VALUES (%s, %s, %s, %s)", 
                                     (username, generate_password_hash(password), gender, S3_url+"avatar/"+avatar  ) )
                
            except db.IntegrityError:
                error = f"L'utilisateur {username} existe déja."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


# login view function
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # get user data from users table
        with db:
            with db.cursor() as curs:
                curs.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = curs.fetchone()

        if user is None:
            error = "L'utilisateur n'existe pas !"
        elif not check_password_hash(user['password'], password):
            error = 'Mot de passe incorrecte !'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# load the function before every request to get user informations
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
         db = get_db()
         with db:
            with db.cursor() as curs:
                curs.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                g.user = curs.fetchone()


# logout 
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# create decorator to check if user is loged when he edit or create new article
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
