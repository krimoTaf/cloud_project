from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import markdown

from tcb.auth import login_required
from tcb.db import get_db

from tcb.comment import get_comment, count_comment
from tcb.likes import count_likes, is_user_liked_post

bp = Blueprint('blog', __name__)


# index of the application return all articles
@bp.route('/')
def index():
    db = get_db()

    with db:
        with db.cursor() as curs:
            curs.execute(
                'SELECT p.id, title, left(body, 1000) as "body", created, author_id, username, avatar'
                ' FROM post p JOIN users u ON p.author_id = u.id'
                ' ORDER BY created DESC')
            posts = curs.fetchall()
    
    
    if g.user is not None:
        for post in posts:
            # convert markdown to html
            post['body'] = markdown.markdown(post['body'])
            post['nb_comment'] = count_comment(post['id'])
            post['nb_likes'] = count_likes(post['id'])
            post['is_liked'] = is_user_liked_post(post['id'], g.user['id'])
    
    else:
        for post in posts:
            # convert markdown to html
            post['body'] = markdown.markdown(post['body'])
            post['nb_comment'] = count_comment(post['id'])
            post['nb_likes'] = count_likes(post['id'])
        
    

    return render_template('blog/index.html', posts=posts)


# create new blog @login_required : login required (auth package)
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    
    if request.method == 'GET':
        images = get_img(g.user['id'])


    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            with db:
                with db.cursor() as curs:
                    curs.execute(
                        'INSERT INTO post (title, body, author_id)'
                        ' VALUES (%s, %s, %s)',
                        (title, body, g.user['id'])
                    )
         
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html', images=images)



def get_img(user_id):
    db = get_db()

    with db:
        with db.cursor() as curs:
            curs.execute(
                'SELECT name, link'
                ' FROM image WHERE user_id = %s'
                ' ORDER BY created DESC',
                (user_id,))
            images = curs.fetchall()
    return images


# get post to use it in update and delete
def get_post(id, check_author=True):
    db = get_db()

    with db:
        with db.cursor() as curs:
            curs.execute(
                'SELECT p.id, title, body, created, author_id, username, avatar'
                ' FROM post p JOIN users u ON p.author_id = u.id'
                ' WHERE p.id = %s',
                (id,)
            )
            post = curs.fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/post')
def read(id):
    post = get_post(id, False)
    post['nb_comment'] = count_comment(post['id'])
    post['nb_likes'] = count_likes(post['id'])
    post['comments'] = get_comment(id)

    # convert markdown to html
    post['body'] = markdown.markdown(post['body'])

    if g.user is not None:
        post['is_liked'] = is_user_liked_post(post['id'], g.user['id'])

    for comment in post['comments']:
        comment['body'] = markdown.markdown(comment['body'])

    return render_template('blog/post.html', post=post)


# edit article
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    post["images"] = get_img(g.user['id'])

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            with db:
                with db.cursor() as curs:
                    curs.execute(
                        'UPDATE post SET title = %s, body = %s WHERE id=%s',
                        (title, body, id)
                    )

            return redirect(url_for('blog.read', id=id))

    return render_template('blog/update.html', post=post)



# delete article
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    
    with db:
        with db.cursor() as curs:
            curs.execute('DELETE FROM likes WHERE post_id = %s', (id,))
            curs.execute('DELETE FROM comment WHERE post_id = %s', (id,))
            curs.execute('DELETE FROM post WHERE id = %s', (id,))

    return redirect(url_for('blog.index'))
