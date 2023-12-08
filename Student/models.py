from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    aadhar = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='student_pics', null=True, blank=True)
    class_level = models.CharField(max_length=50)
    address = models.TextField()
    section = models.CharField(max_length=10)

    def __str__(self):
        return self.name
