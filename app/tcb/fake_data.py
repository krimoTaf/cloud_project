from faker import Faker
from mdgen import MarkdownPostProvider
from werkzeug.security import generate_password_hash
import random
from tcb.upload_s3 import upload_S3
from tcb.download_avatar import download_avatar
from flask import current_app




# generate faka data to our differents tables
def genrate_fake_data(db):
    fake = Faker()
    fake.add_provider(MarkdownPostProvider)


    S3_url = current_app.config['AWS_S3_LINK']

    users = []
    posts = []
    comments = []
    likes = []

    for _ in range(10):
        gender = random.choice(["male","female"])
        username = fake.name()

        avatar = download_avatar(gender, username.replace(" ", ""))
        upload_S3(avatar, "tcb-cloud", "avatar/"+avatar)

        users.append((username, generate_password_hash("test123"), gender, S3_url+"avatar/"+avatar))
        posts.append((fake.text()[:10] , fake.post(size='large'), random.randint(1,10)))
        comments.append( (random.randint(1,10), random.randint(1,10), fake.text()))
        likes.append((random.randint(1,10), random.randint(1,10)))

    with db:
        with db.cursor() as curs:
            # users
            curs.executemany("INSERT INTO users (username, password, gender, avatar) VALUES (%s, %s, %s, %s)", users)
            #posts
            curs.executemany('INSERT INTO post (title, body, author_id) VALUES (%s, %s, %s)', posts)
            #comments
            curs.executemany('INSERT INTO comment (user_id, post_id, body) VALUES (%s, %s, %s)', comments)
            #likes
            curs.executemany('INSERT INTO likes (user_id, post_id) VALUES (%s, %s)', likes)