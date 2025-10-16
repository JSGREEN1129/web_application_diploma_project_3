from django.db import models
from projects.models import Project
from django.utils import timezone


class Task(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('outstanding', 'Outstanding'),
        ('overdue', 'Overdue'),
    ]

    project = models.ForeignKey(
        Project, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=11, choices=STATUS_CHOICES, default='outstanding')
    previous_status = models.CharField(
        max_length=11, choices=STATUS_CHOICES, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Task: {self.name}"

    def check_status(self):
        """
        Update the status to 'overdue' if past end_date and not completed,
        else set to 'outstanding'.
        """
        if self.status == 'completed':
            return

        if self.end_date and self.end_date < timezone.now().date():
            self.status = 'overdue'
        else:
            self.status = 'outstanding'
        self.save()

    def toggle_complete(self):
        """
        Toggle the completion status of the task.
        If completed, mark as outstanding or overdue based on date.
        If not completed, mark as completed and set completed_at.
        """
        if self.status == 'completed':
            if self.end_date and self.end_date < timezone.now().date():
                self.status = 'overdue'
            else:
                self.status = 'outstanding'
            self.completed_at = None
        else:
            self.status = 'completed'
            self.completed_at = timezone.now()
        self.save()
