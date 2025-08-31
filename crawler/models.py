from django.db import models

class Config(models.Model):
    protocol = models.CharField(max_length=50)
    config_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.protocol} - {self.id}"