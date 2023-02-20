"""Seed file to make sample data for pets db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
macho = User(first_name='Macho', last_name='Man', image_url='https://media.npr.org/assets/img/2011/05/21/ap110520018042_custom-8fbb1ec5b25461f081f09a9464d46e66962126a4-s300-c85.webp')
ultimate = User(first_name='Ultimate', last_name='Warrior', image_url='https://www.nicepng.com/png/detail/185-1850458_the-ultimate-warrior-png-photos-ultimate-warrior-wwe.png')
rey = User(first_name='Rey', last_name='Mysterio', image_url='https://www.pwmania.com/wp-content/uploads/2012/07/rey-mysterio.jpg')

p1 = Post(title="post one", content="Here is some content for 'ya", user=macho)
p2 = Post(title="post two", content="Here is some content for 'ya", user=macho)
p3 = Post(title="post three", content="Here is some content for 'ya", user=macho)
p4 = Post(title="post four", content="Here is some content for 'ya", user=rey)

db.session.add(macho)
db.session.add(ultimate)
db.session.add(rey)

# Commit--otherwise, this never gets saved!
db.session.commit()
