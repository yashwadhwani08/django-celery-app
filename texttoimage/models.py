from django.db import models

# Create your models here.
class PromptToImage(models.Model):
    text_input = models.CharField(max_length=10000)
    meta_data = models.JSONField(blank=True, null=True)
    image_output = models.ImageField(blank=True)
