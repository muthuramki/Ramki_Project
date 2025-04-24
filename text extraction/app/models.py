from django.db import models
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    
    def __str__(self):
        return self.title