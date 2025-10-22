from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.core.exceptions import ValidationError
from django.urls import reverse


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

# User registration and Login test code        
class UserViewTests(TestCase):
    def test_register_view_get(self):
        """GET request to registration view returns 200 and correct template."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post_valid_data_creates_user(self):
        """POST valid data to register view creates a user and redirects."""
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'VerySecurePassword123!',
            'password2': 'VerySecurePassword123!',
            'register_submit': 'Register'
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())

    def test_register_view_post_invalid_data(self):
        """POST invalid data returns form errors."""
        form_data = {
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email',
            'password1': '123',
            'password2': '456',
        }
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertFalse(User.objects.exists())

    def test_login_view_get(self):
        """GET request to login view returns 200."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post_valid_credentials(self):
        """POST valid credentials logs in the user."""
        user = User.objects.create_user(username='loginuser', email='loginuser@example.com', password='MyStrongPass123')
        form_data = {
            'username': 'loginuser@example.com',
            'password': 'MyStrongPass123',
                'login_submit': 'Login'
        }
        response = self.client.post(reverse('login'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid_credentials(self):
        """POST invalid credentials returns error."""
        form_data = {
            'username': 'wrong@example.com',
            'password': 'wrongpass',
        }
        response = self.client.post(reverse('login'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No account found with this email.')
