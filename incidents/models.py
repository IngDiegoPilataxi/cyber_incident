from django.db import models

# Create your models here.


class Incident(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-reported_at'] # Newest first