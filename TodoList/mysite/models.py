from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь",related_name="blogs")
    title = models.CharField(max_length=20, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание блога")
    date = models.DateField(verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'blogs'
        verbose_name='Блог'
        verbose_name_plural = 'Блоги'
        ordering = ['-date']

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Пользователь",related_name="user_comments")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,verbose_name="Блог",related_name="blog_comments")
    comment = models.TextField(verbose_name="Комментарий")
    date = models.DateField(verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий от {self.user.username}"

    class Meta:
        db_table = 'comments'
        ordering = ['-date']
        verbose_name='Комментарий'
        verbose_name_plural = 'Комментарии'