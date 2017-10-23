from django.db import models
import re, bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate_user_r(self,post_data):
        response_to_views ={}
        TheUser=self.filter(email=post_data['email'])
        if TheUser:
            response_to_views['status']=False
            return response_to_views
        email_Match=re.compile(r'[^@]+@[^@]+\.[^@]+')
        name_Match=re.compile(r'^[a-zA-Z]{2,255}$')
        input_valid=True
        if not re.match(name_Match, post_data['fname']):
            input_valid=False
        if not re.match(name_Match, post_data['lname']):
            input_valid=False
        if not re.match(email_Match, post_data['email']):
            input_valid=False
        if len(post_data['p'])<8 and post_data['p']!= post_data['cp']:
            input_valid=False
        if input_valid:
            new_user = self.create(
            fname=post_data['fname'],
            lname=post_data['lname'],
            email=post_data['email'],
            password=bcrypt.hashpw(post_data['p'].encode(), bcrypt.gensalt())
            )
            response_to_views['status']=True
            response_to_views['id']=new_user.id
            return response_to_views
        response_to_views['status']=False
        return response_to_views
    def validate_user_l(self, post_data):
        response_to_views={}
        TheUser=self.filter(email=post_data['lemail'])
        if TheUser:
            if bcrypt.checkpw(post_data['lp'].encode(), TheUser[0].password.encode()):
                response_to_views['status']=True
                response_to_views['id']=TheUser[0].id
                return response_to_views
        response_to_views['status']=False
        return response_to_views

class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
