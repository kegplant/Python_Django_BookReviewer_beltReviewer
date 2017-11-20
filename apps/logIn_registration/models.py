from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from django.db import models
class UserManager(models.Manager):
    def registration_validator(self,postData):
        errors={}
        users=self.filter(email=postData['email'])
        if users:
            errors['email']='account already exists'
        elif len(postData['first_name'])<2:
            errors['name']='first name should be no fewer than 2 characters!'
        elif len(postData['last_name'])<2:
            errors['name']='last name should be no fewer than 2 characters!'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email']='invalid email!'
        elif len(postData['password'])<9:
            errors['password']='password should be no fewer than 8 characters!'
        elif postData['password']!=postData['password2']:
            errors['password']='passwords should match!'
        return errors
    def logIn_validator(self,postData):
        errors={}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']='invalid email!'
        else:
            users=Users.objects.filter(email=postData['email'])
            if not users:
                errors['email']='something wrong about email / password'
            elif not bcrypt.checkpw(postData['password'].encode(),users[0].password.encode()):
                errors['email']='something wrong about email / password'
        return errors
class BookManager(models.Manager):
    def createBook(self,postData):
        book=self.create(title=postData['title'],author=postData['selectAuthor'])
        return book
# Create your models here.
class Users(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255,default='')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    # books=models.ManyToManyField(Books,related_name='authors')
    # notes=models.TextField(default='')
class Books(models.Model):
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=255)
    objects=BookManager()
class Reviews(models.Model):
    user=models.ForeignKey(Users,related_name='reviews')
    book=models.ForeignKey(Books,related_name='reviews')
    rating=models.IntegerField(max_length=1)
    review=models.TextField()
    created_at=models.DateField(auto_now_add=True)


