from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Project
from datetime import date, timedelta
from django.utils.http import urlencode

class ProjectViewTests(TestCase):
    def setUp(self):
        # Create two users
        self.user = User.objects.create_user('user', 'user@example.com', 'pass')
        self.other_user = User.objects.create_user('other', 'other@example.com', 'pass2')

        # Log in as the main user
        self.client.login(username='user', password='pass')

        # Create a project owned by the logged-in user
        self.project = Project.objects.create(
            name='My Project',
            description='Test project',
            owner=self.user,
            status='open',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7)
        )

        # Create another project owned by a different user
        self.other_project = Project.objects.create(
            name='Other Project',
            description='Other user project',
            owner=self.other_user,
            status='open',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7)
        )

    def project_data(self, overrides=None):
        """Helper to build complete project form data"""
        base = {
            'name': 'New Project',
            'description': 'Some description',
            'status': 'open',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=10),
        }
        if overrides:
            base.update(overrides)
        return base

    def test_project_create_get(self):
        """GET request to project_create should return form page."""
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_create.html')

    def test_project_create_post_valid(self):
        """Valid POST should create project and redirect to list view."""
        data = self.project_data()
        response = self.client.post(reverse('project_create'), data)
        self.assertRedirects(response, reverse('project_list'))
        self.assertTrue(Project.objects.filter(name='New Project', owner=self.user).exists())

    def test_project_create_post_invalid(self):
        """Invalid POST (e.g., missing name) should return form errors."""
        data = self.project_data({'name': ''})
        response = self.client.post(reverse('project_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    def test_project_list_shows_only_user_projects(self):
        """User should only see their own projects in the list view."""
        response = self.client.get(reverse('project_list'))
        projects = response.context['projects']
        self.assertIn(self.project, projects)
        self.assertNotIn(self.other_project, projects)

    def test_project_detail_owner_access(self):
        """Project owner should be able to view their project detail page."""
        response = self.client.get(reverse('project_detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['project'], self.project)

    def test_project_detail_forbidden_to_other_user(self):
        """Users should not be able to view other users' project details."""
        response = self.client.get(reverse('project_detail', args=[self.other_project.id]))
        self.assertEqual(response.status_code, 404)

    def test_project_edit_get(self):
        """GET request to edit should load the form with current project data."""
        response = self.client.get(reverse('project_edit', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_edit.html')

    def test_project_edit_post_valid(self):
        """Valid POST should update the project and redirect to detail."""
        data = self.project_data({'name': 'Updated Project'})
        response = self.client.post(reverse('project_edit', args=[self.project.id]), data)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Project')
        self.assertRedirects(response, reverse('project_detail', kwargs={'project_id': self.project.id}))

    def test_project_edit_post_invalid(self):
        """Invalid data should keep user on form page with errors."""
        data = self.project_data({'name': ''})
        response = self.client.post(reverse('project_edit', args=[self.project.id]), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    def test_project_delete_with_correct_password(self):
        """Correct password should delete the project."""
        response = self.client.post(reverse('project_confirm_delete', args=[self.project.id]), {'password': 'pass'})
        self.assertRedirects(response, reverse('project_list'))
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_project_delete_with_wrong_password(self):
        """Wrong password should not delete the project and return error message."""
        response = self.client.post(reverse('project_confirm_delete', args=[self.project.id]), {'password': 'wrong'})
        expected_url = reverse('project_list') + '?' + urlencode({
            'error_project_id': self.project.id,
            'error_message': 'Incorrect password. Project not deleted.'
        })
        self.assertRedirects(response, expected_url)
        self.assertTrue(Project.objects.filter(id=self.project.id).exists())

    def test_project_toggle_complete_marks_project_and_tasks_completed(self):
        """Closing a project should also mark all tasks as completed."""
        task1 = self.project.tasks.create(name='Task 1', status='outstanding')
        task2 = self.project.tasks.create(name='Task 2', status='outstanding')

        response = self.client.get(reverse('project_toggle_complete', args=[self.project.id]))
        self.project.refresh_from_db()
        task1.refresh_from_db()
        task2.refresh_from_db()

        self.assertEqual(self.project.status, 'closed')
        self.assertEqual(task1.status, 'completed')
        self.assertEqual(task2.status, 'completed')

    def test_project_toggle_complete_reopens_tasks(self):
        """Reopening a closed project should restore original task statuses."""
        task1 = self.project.tasks.create(name='Task 1', status='completed')
        task2 = self.project.tasks.create(name='Task 2', status='completed')

        # Simulate previous statuses saved
        self.project.status = 'closed'
        self.project.previous_task_statuses = {
            str(task1.id): 'outstanding',
            str(task2.id): 'outstanding',
        }
        self.project.save()

        response = self.client.get(reverse('project_toggle_complete', args=[self.project.id]))
        self.project.refresh_from_db()
        task1.refresh_from_db()
        task2.refresh_from_db()

        self.assertEqual(self.project.status, 'open')
        self.assertEqual(task1.status, 'outstanding')
        self.assertEqual(task2.status, 'outstanding')

    def test_protected_views_redirect_anonymous(self):
        """Anonymous users should be redirected to login for protected views."""
        self.client.logout()
        protected_urls = [
            reverse('project_create'),
            reverse('project_list'),
            reverse('project_detail', args=[self.project.id]),
            reverse('project_edit', args=[self.project.id]),
            reverse('project_confirm_delete', args=[self.project.id]),
            reverse('project_toggle_complete', args=[self.project.id]),
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse('login'), response.url)
