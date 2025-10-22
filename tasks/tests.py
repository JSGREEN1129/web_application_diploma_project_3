from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth.models import User
from projects.models import Project
from tasks.models import Task

class TaskModelTests(TestCase):
    def setUp(self):
        """
        Set up a user and a test project before each test.
        This ensures every test has access to a valid user and project.
        """
        self.user = User.objects.create_user(username='tester', password='pass')
        self.project = Project.objects.create(
            name='Test Project',
            description='For task tests',
            owner=self.user,
            status='open',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=5)
        )

    def create_task(self, **kwargs):
        defaults = {
            'project': self.project,
            'name': 'Test Task',
            'description': 'Test description',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=1),
            'status': 'outstanding'
        }
        defaults.update(kwargs)
        return Task.objects.create(**defaults)

    def test_task_creation_defaults(self):
        """
        Test default values of a newly created task.
        """
        task = self.create_task()
        self.assertEqual(task.status, 'outstanding')  # Default status should be 'outstanding'
        self.assertIsNone(task.completed_at)  # Task should not be completed
        self.assertEqual(task.project, self.project)  # Should be assigned to the correct project

    def test_check_status_sets_overdue_if_past_due(self):
        """
        If task end date is in the past and it's not completed, status should become 'overdue'.
        """
        task = self.create_task(end_date=date.today() - timedelta(days=1))
        task.check_status()
        self.assertEqual(task.status, 'overdue')

    def test_check_status_sets_outstanding_if_not_overdue(self):
        """
        If the task was marked 'overdue' but the end date is in the future,
        `check_status` should correct it to 'outstanding'.
        """
        task = self.create_task(end_date=date.today() + timedelta(days=1))
        task.status = 'overdue'
        task.save()
        task.check_status()
        self.assertEqual(task.status, 'outstanding')

    def test_check_status_does_nothing_if_completed(self):
        """
        If the task is already completed, `check_status` should not change it.
        """
        task = self.create_task(status='completed')
        task.check_status()
        self.assertEqual(task.status, 'completed')

    def test_check_status_with_no_end_date_sets_outstanding(self):
        """
        If no end date is provided and the task is not completed, it should be set to 'outstanding'.
        """
        task = self.create_task(end_date=None)
        task.status = 'overdue'
        task.save()
        task.check_status()
        self.assertEqual(task.status, 'outstanding')

    def test_toggle_complete_marks_as_completed(self):
        """
        When toggling from 'outstanding' to 'completed', the status and completed_at timestamp should update.
        """
        task = self.create_task(status='outstanding')
        task.toggle_complete()
        self.assertEqual(task.status, 'completed')
        self.assertIsNotNone(task.completed_at)

    def test_toggle_complete_from_completed_sets_overdue_if_late(self):
        """
        When toggling a completed task with a past end date,
        it should become 'overdue' and completed_at should be cleared.
        """
        task = self.create_task(
            status='completed',
            completed_at=timezone.now(),
            end_date=date.today() - timedelta(days=1)
        )
        task.toggle_complete()
        self.assertEqual(task.status, 'overdue')
        self.assertIsNone(task.completed_at)

    def test_toggle_complete_from_completed_sets_outstanding_if_on_time(self):
        """
        When toggling a completed task whose end date is in the future,
        it should become 'outstanding' again.
        """
        task = self.create_task(
            status='completed',
            completed_at=timezone.now(),
            end_date=date.today() + timedelta(days=1)
        )
        task.toggle_complete()
        self.assertEqual(task.status, 'outstanding')
        self.assertIsNone(task.completed_at)

    def test_toggle_complete_from_completed_sets_outstanding_if_no_end_date(self):
        """
        When a completed task has no end date and is toggled,
        it should become 'outstanding'.
        """
        task = self.create_task(status='completed', completed_at=timezone.now(), end_date=None)
        task.toggle_complete()
        self.assertEqual(task.status, 'outstanding')
        self.assertIsNone(task.completed_at)
