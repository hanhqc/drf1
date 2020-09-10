from django.db import models

# Create your models here.

class User(models.Model):
    gender_choices = (
        (0, 'male'),
        (1, 'female'),
        (2, 'other'),
    )

    name = models.CharField(max_length=40)
    pwd = models.CharField(max_length=40)
    gender = models.SmallIntegerField(choices=gender_choices, default=0)

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name