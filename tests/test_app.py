import unittest
from app import create_app
from app.models import User, ElectronicProduct
from app import db

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenue', response.data)

    def test_create_user(self):
        user = User(username='testuser', password='testpass', role='user')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(User.query.filter_by(username='testuser').first())

    def test_create_product(self):
        product = ElectronicProduct(
            name='Test Product',
            description='A test product',
            price=99.99,
            brand='Test Brand',
            model_number='TEST123',
            category='Test Category',
            stock=10
        )
        db.session.add(product)
        db.session.commit()
        self.assertIsNotNone(ElectronicProduct.query.filter_by(name='Test Product').first())

    def test_user_password(self):
        user = User(username='testuser', password='testpass', role='user')
        user.set_password('newpassword')
        self.assertTrue(user.check_password('newpassword'))
        self.assertFalse(user.check_password('testpass'))

if __name__ == '__main__':
    unittest.main()
