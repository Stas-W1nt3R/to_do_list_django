from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blogs'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'comments'