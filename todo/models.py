from django.db import models

from datetime import datetime

# Create your models here.
class Task(models.Model):

    name = models.CharField(max_length = 255)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField()
    STATUS_CHOICES = [
        (1, 'To Do'),
        (2, 'In Progress'),
        (3, 'Completed'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return f"Name: {self.name}, Start Date: {self.start_date}, End Date: {self.end_date}"
    
    def get_all_values_to_dict(self):
        vars(self).pop('_state')
        return vars(self)

