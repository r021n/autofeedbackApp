from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topics(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    
    def __str__(self):
        return self.name
    
class Questions(models.Model):
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, blank=True, null=True)
    question = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(null=True, upload_to='appBelajar/templates/upload', blank=True)
    image_description = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.question
    
class Answers1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    score = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.answer} {self.feedback}"

class Answers2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    score = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.answer} {self.feedback}"

class Answers3(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    score = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.answer} {self.feedback}"