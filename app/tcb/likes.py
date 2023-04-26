from tcb.db import get_db

from flask import (
    Blueprint, g, request, url_for
)

bp = Blueprint('likes', __name__)

# count number of likes on the post
def count_likes(post_id):
    db = get_db()

    with db:
        with db.cursor() as curs:
            curs.execute(
                'SELECT count(*) as "nb_like" FROM likes l'
                ' WHERE l.post_id = %s',
                (post_id,)
            )
            nb_likes = curs.fetchone()


    return nb_likes["nb_like"]


# check if post is licked by user
def is_user_liked_post(post_id, user_id):
    db = get_db()

    with db:
        with db.cursor() as curs:
            curs.execute(
                'SELECT * FROM likes l'
                ' WHERE l.post_id = %s and l.user_id = %s',
                (post_id, user_id)
            )
            likes = curs.fetchone()


    return True if likes else False



# dislike
@bp.route('/dislike', methods=('POST',))
def delete():
    if request.method == 'POST':
        post_id = request.form['post_id']
        user_id = request.form['user_id']
    
        db = get_db()
        with db:
            with db.cursor() as curs:
                curs.execute('DELETE FROM likes WHERE post_id = %s AND user_id = %s', (post_id, user_id))

        return "Post "+post_id+" disliked !"
    
    return "Probleme occured when we try to dislike post" + post_id


# like
@bp.route('/like', methods=('POST',))
def create():
    if request.method == 'POST':
        post_id = request.form['post_id']
        user_id = request.form['user_id']
    
        db = get_db()
        with db:
            with db.cursor() as curs:
                curs.execute('INSERT INTO likes (user_id, post_id) VALUES (%s, %s)', (user_id, post_id))

        return "Post "+post_id+" liked !"
    
    return "Probleme occured when add like to post" + post_id
