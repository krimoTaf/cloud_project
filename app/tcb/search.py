from flask import (
    Blueprint, g, render_template, request
)

import markdown

from tcb.db import get_db

from tcb.db import get_db

from tcb.comment import count_comment
from tcb.likes import count_likes, is_user_liked_post

bp = Blueprint('search', __name__)



@bp.route('/', methods=['POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        search = search.join(['%', '%'])

        db = get_db()

        with db:
            with db.cursor() as curs:
                curs.execute(
                    'SELECT p.id, title, left(body, 1000) as "body", created, author_id, username, avatar'
                    ' FROM post p JOIN users u ON p.author_id = u.id'
                    ' WHERE LOWER(title) LIKE LOWER(%s) OR LOWER(body) like LOWER(%s)'
                    ' ORDER BY created DESC',
                    (search, search))
                
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