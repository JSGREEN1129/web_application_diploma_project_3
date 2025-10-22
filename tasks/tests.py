from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth.models import User
from projects.models import Project
from tasks.models import Task

class TaskModelTests(TestCase):
    def setUp(self):
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
        task = self.create_task()
        self.assertEqual(task.status, 'outstanding')
        self.assertIsNone(task.completed_at)
        self.assertEqual(task.project, self.project)

    def test_check_status_sets_overdue_if_past_due(self):
        task = self.create_task(end_date=date.today() - timedelta(days=1))
        task.check_status()
        self.assertEqual(task.status, 'overdue')

    def test_check_status_sets_outstanding_if_not_overdue(self):
        task = self.create_task(end_date=date.today() + timedelta(days=1))
        task.status = 'overdue'
        task.save()
        task.check_status()
        self.assertEqual(task.status, 'outstanding')

    def test_check_status_does_nothing_if_completed(self):
        task = self.create_task(status='completed')
        task.check_status()
        self.assertEqual(task.status, 'completed')

    def test_check_status_with_no_end_date_sets_outstanding(self):
        task = self.create_task(end_date=None)
        task.status = 'overdue'
        task.save()
        task.check_status()
        self.assertEqual(task.status, 'outstanding')

    def test_toggle_complete_marks_as_completed(self):
        task = self.create_task(status='outstanding')
        task.toggle_complete()
        self.assertEqual(task.status, 'completed')
        self.assertIsNotNone(task.completed_at)

    def test_toggle_complete_from_completed_sets_overdue_if_late(self):
        task = self.create_task(
            status='completed',
            completed_at=timezone.now(),
            end_date=date.today() - timedelta(days=1)
        )
        task.toggle_complete()
        self.assertEqual(task.status, 'overdue')
        self.assertIsNone(task.completed_at)

    def test_toggle_complete_from_completed_sets_outstanding_if_on_time(self):
        task = self.create_task(
            status='completed',
            completed_at=timezone.now(),
            end_date=date.today() + timedelta(days=1)
        )
        task.toggle_complete()
        self.assertEqual(task.status, 'outstanding')
        self.assertIsNone(task.completed_at)

    def test_toggle_complete_from_completed_sets_outstanding_if_no_end_date(self):
        task = self.create_task(status='completed', completed_at=timezone.now(), end_date=None)
        task.toggle_complete()
        self.assertEqual(task.status, 'outstanding')
        self.assertIsNone(task.completed_at)
