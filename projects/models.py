from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='projects')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='open')
    start_date = models.DateField()
    end_date = models.DateField()

    previous_task_statuses = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

    def update_task_counts(self):
        """Update task count attributes for this project instance."""
        self.completed_count = self.tasks.filter(status="completed").count()
        self.outstanding_count = self.tasks.filter(
            status="outstanding").count()
        self.overdue_count = self.tasks.filter(status="overdue").count()
        self.total_tasks = self.tasks.count()
