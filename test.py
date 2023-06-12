from app import app
from models import db, connect_db, User
from unittest import TestCase

# New test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserRoutesTestCase(TestCase):
    
    def setUp(self):
        """adds sample user"""
        User.query.delete()
        
        user = User(first_name='Kevin', last_name='Nichols')
        db.session.add(user)
        db.session.commit()
        
        self.user_id = user.id
        
    def tearDown(self):
        """Clean up"""
        db.session.rollback()
        
    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 302)
            
    def test_new_user_page(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Create user</h1>', html)
            
    def test_edit_user_page(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}/edit')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Edit your profile</h1>', html)
            
    def test_user_page(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Kevin Nichols</h1>', html)           