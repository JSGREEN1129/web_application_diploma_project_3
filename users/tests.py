from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.core.exceptions import ValidationError


class CustomUserCreationFormTest(TestCase):
    def test_form_valid_data_creates_user(self):
        form_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'password1': 'strongPassword123',
            'password2': 'strongPassword123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, 'alice@example.com')
        self.assertEqual(User.objects.count(), 1)

    def test_form_raises_error_if_email_exists_on_save(self):
        User.objects.create_user(username='existinguser', email='duplicate@example.com', password='123456')

        form_data = {
            'first_name': 'Bob',
            'last_name': 'Jones',
            'email': 'duplicate@example.com',
            'password1': 'Thisisthefirstpasswordfortesting',
            'password2': 'Thisisthefirstpasswordfortesting'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid()) 

        with self.assertRaises(ValidationError) as context:
            form.save()

        self.assertIn("A user with this email already exists.", str(context.exception))

    def test_form_invalid_password_mismatch(self):
        form_data = {
            'first_name': 'Charlie',
            'last_name': 'Brown',
            'email': 'charlie@example.com',
            'password1': 'Thisisthesecondpasswordfortesting',
            'password2': 'Thisisthepasswordfortesting'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class CustomAuthenticationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', email='login@example.com', password='testpass123')

    def test_login_with_valid_credentials(self):
        form_data = {
            'username': 'login@example.com',
            'password': 'testpass123'
        }
        form = CustomAuthenticationForm(None, data=form_data)
        self.assertTrue(form.is_valid())

        user = authenticate(username=self.user.username, password='testpass123')
        self.assertIsNotNone(user)

    def test_login_with_nonexistent_email(self):
        form_data = {
            'username': 'nonexistent@example.com',
            'password': 'whatever'
        }
        form = CustomAuthenticationForm(None, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('No account found with this email.', form.errors['username'])

    def test_login_with_wrong_password(self):
        form_data = {
            'username': 'login@example.com',
            'password': 'wrongpass'
        }
        form = CustomAuthenticationForm(None, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
