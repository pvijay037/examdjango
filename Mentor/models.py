from django.db import models

class Mentor(models.Model):
    mentor_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.mentor_code

class Student(models.Model):
    email = models.EmailField(unique=True)
    mentor = models.ForeignKey(Mentor, related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return self.email
