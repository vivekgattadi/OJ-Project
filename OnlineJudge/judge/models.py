from statistics import mode
from tkinter import CASCADE
from django.db import models

# Create your models here.
class Problem(models.Model):
    #https://stackoverflow.com/questions/40870145/django-charfield-with-no-max-length
    statement = models.TextField() 
    name = models.CharField(max_length=200)
    code = models.TextField()
    difficulty = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=100)
    submitted_at = models.DateTimeField('date published')
    submitted_code = models.TextField(default='something')

    def __str__(self):
        return self.verdict

class TestCase(models.Model):
    input_test = models.TextField()
    output_test = models.TextField()
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return self.input_test
    