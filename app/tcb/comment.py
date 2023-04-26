from tcb.db import get_db

from flask import (
    Blueprint, g, request, url_for
)

bp = Blueprint('comment', __name__)

# get comment
def get_comment(post_id, check_author=False):
    db = get_db()

    with db:
        with db.cursor() as curs:
            curs.execute(
                'SELECT c.id, c.user_id, u.username, u.avatar, c.body, c.created'
                ' FROM comment c LEFT JOIN users u ON c.user_id = u.id'
                ' WHERE c.post_id = %s'
                'ORDER BY created',
                (post_id,)
            )
            comments = curs.fetchall()

    return comments


# count number of comment on the post
def count_comment(post_id):
    db = get_db()

    with db:
        with db.cursor() as curs:
            curs.execute(
                'SELECT count(*) as "nb_comment" FROM comment c'
                ' WHERE c.post_id = %s',
                (post_id,)
            )
            nb_comment = curs.fetchone()


    return nb_comment["nb_comment"]



# add new comment
@bp.route('/comment', methods=('POST',))
def create():
    if request.method == 'POST':
        post_id = request.form['post_id']
        user_id = request.form['user_id']
        body = request.form['body']
    
        db = get_db()

        with db:
            with db.cursor() as curs:
                curs.execute('INSERT INTO comment (user_id, post_id, body) VALUES (%s, %s, %s)', (user_id, post_id, body))
                curs.execute("SELECT LASTVAL();")
                comment_id = dict(curs.fetchone())


        return {'comment_id': comment_id['lastval'], 'user_id': user_id}
    
    return "Probleme when add comment !"


# delete comment
@bp.route('/delete_comment', methods=('POST',))
def delete():
    if request.method == 'POST':
        id = request.form['id']
        user_id = request.form['user_id']
    
        db = get_db()
        with db:
            with db.cursor() as curs:
                curs.execute('DELETE FROM comment WHERE id = %s AND user_id = %s', (id, user_id))

        return "Comment of post "+id+" deleted !"
    
    return "Probleme occured when we try to delete comment of post " + id
