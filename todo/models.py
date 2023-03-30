from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["completed"]