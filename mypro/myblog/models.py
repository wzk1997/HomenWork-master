from django.db import models
from  tinymce.models import HTMLField

class Management(models.Manager):
    def regulate(self, name, password):
        self.create(name=name, password=password)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    # avatar = models.CharField(max_length=255,default='myblog/images')
    # man = Management()
    avatar= models.ImageField(upload_to='static/images/')

    def __str__(self):
        a=self.name
        return a
    @classmethod
    def reg(cls, name, password):
        um = cls(name=name, password=password)
        return um


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    coutext = HTMLField()
    author = models.ForeignKey(User)

    def __str__(self):
        a=self.title
        return a
    @classmethod
    def text(cls, title, coutext):
        T = cls(title=title, coutext=coutext)
        return T

# Create your models here.
