from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    # Choices for the status field
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    # Project title
    name = models.CharField(max_length=200)

    # Full project description
    description = models.TextField()

    # Reference to the user who owns the project
    owner = models.ForeignKey(
        # If the user is deleted, delete their projects too
        User, on_delete=models.CASCADE, related_name='projects')

    # Status of the project - 'open' or 'closed'
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='open')

    # Start and end dates for the project
    start_date = models.DateField()
    end_date = models.DateField()

    # JSON storage for task status snapshots
    previous_task_statuses = models.JSONField(null=True, blank=True)

    def __str__(self):
        # What to display when the project is printed
        return self.name

    def update_task_counts(self):
        """
        Dynamically add task-related counters to this instance:
        - completed_count: tasks marked as completed
        - outstanding_count: tasks still pending
        - overdue_count: tasks past due
        - total_tasks: total number of tasks
        """
        self.completed_count = self.tasks.filter(status="completed").count()
        self.outstanding_count = self.tasks.filter(
            status="outstanding").count()
        self.overdue_count = self.tasks.filter(status="overdue").count()
        self.total_tasks = self.tasks.count()
