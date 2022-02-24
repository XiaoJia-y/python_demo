from tkinter.messagebox import YES
from django.db import models    

class Data(models.Model):
    name = models.CharField(max_length=200)
    href = models.CharField(max_length=200)
    price = models.CharField(max_length=20)
    agree = models.CharField(max_length=20, null=YES)
    people = models.CharField(max_length=20, null=YES)
    about = models.CharField(max_length=20, null=YES)

class Login_table(models.Model):
    user_name = models.CharField(max_length = 18)
    pass_word = models.CharField(max_length = 18)
    
class User_table(models.Model):
    name = models.CharField(max_length = 20)
    user_name = models.CharField(max_length = 20)
    pass_word = models.CharField(max_length = 20)
