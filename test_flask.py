from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views of users"""

    def setUp(self):
        """Add sample user"""
        Post.query.delete()
        User.query.delete()
        

        user = User(first_name='userone', last_name='testlastname', image_url='https://b2059463.smushcdn.com/2059463/wp-content/uploads/2019/09/crash-testing-dummies1-150x150.jpg?lossy=1&strip=1&webp=1?lossy=1&strip=1&webp=1https://b2059463.smushcdn.com/2059463/wp-content/uploads/2019/09/crash-testing-dummies1-150x150.jpg?lossy=1&strip=1&webp=1?lossy=1&strip=1&webp=1')
    
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up and fouled transaction"""

        db.session.rollback()
        
    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('userone', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('userone', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {'first_name': 'usertwo', 'last_name': 'testlastname2', 'image_url': 'https://b2059463.smushcdn.com/2059463/wp-content/uploads/2019/09/crash-testing-dummies1-150x150.jpg?lossy=1&strip=1&webp=1?lossy=1&strip=1&webp=1https://b2059463.smushcdn.com/2059463/wp-content/uploads/2019/09/crash-testing-dummies1-150x150.jpg?lossy=1&strip=1&webp=1?lossy=1&strip=1&webp=1'}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('usertwo', html)
    
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertNotIn('userone', html)

class PostViewsTestCase(TestCase):
    """Tests for views for posts"""
    def setUp(self):
        Post.query.delete()
        User.query.delete()
        
        user = User(first_name='postuser', last_name='post_last', image_url='https://b2059463.smushcdn.com/2059463/wp-content/uploads/2019/09/crash-testing-dummies1-150x150.jpg?lossy=1&strip=1&webp=1?lossy=1&strip=1&webp=1https://b2059463.smushcdn.com/2059463/wp-content/uploads/2019/09/crash-testing-dummies1-150x150.jpg?lossy=1&strip=1&webp=1?lossy=1&strip=1&webp=1')
        post = Post(title='Post Title', content='Test Content', user=user)

        db.session.add_all([user, post])
        db.session.commit()

        self.user_id = user.id
        self.user = user
        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up and fouled transaction"""

        db.session.rollback()

    def test_show_posts(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Post Title', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Post Title', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {'title': 'Title two', 'content': 'more content for you'}
            resp = client.post(f'/users/{self.user_id}/posts/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Title two', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Post Title', html)
