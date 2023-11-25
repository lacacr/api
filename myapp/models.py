# myapp/models.py
from django.db import models

class SearchHistory(models.Model):
    query = models.CharField(max_length=255)
    place_name = models.CharField(max_length=255)
    formatted_address = models.TextField()
    place_id = models.CharField(max_length=255)
    distance = models.IntegerField(default=0)  # New field for storing distance

    def __str__(self):
        return f"{self.query} - {self.place_name}"
