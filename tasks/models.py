from django.db import models
from projects.models import Project
from django.utils import timezone


class Task(models.Model):
    # Define choices for task status
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('outstanding', 'Outstanding'),
        ('overdue', 'Overdue'),
    ]

    # ForeignKey to Project, establishing a relationship; deleting project deletes its tasks
    project = models.ForeignKey(
        Project, related_name='tasks', on_delete=models.CASCADE)
    
    # Task name, max length 200 characters
    name = models.CharField(max_length=200)

    # Optional detailed description of the task
    description = models.TextField(blank=True)

    # Start and end dates of the task; both optional
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Current status of the task, defaults to 'outstanding'
    status = models.CharField(
        max_length=11, choices=STATUS_CHOICES, default='outstanding')
    
    # Stores previous status, useful for toggling or restoring status
    previous_status = models.CharField(
        max_length=11, choices=STATUS_CHOICES, null=True, blank=True)
    
    # Timestamp for when task was completed, optional
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        # String representation of the task for admin or debugging
        return f"Task: {self.name}"

    def check_status(self):
        """
        Updates task status based on current date and completion:
        - If already 'completed', do nothing.
        - If past end_date and not completed, set status to 'overdue'.
        - Otherwise, set status to 'outstanding'.
        Then saves the model.
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
        Toggles completion state:
        - If currently 'completed', revert to 'outstanding' or 'overdue' based on end_date.
        - If not completed, mark as 'completed' and set completed_at to now.
        Saves the updated state.
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
