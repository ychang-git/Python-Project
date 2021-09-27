from django.db import models
import bcrypt
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
FNAME_REGEX = re.compile(r'^[a-zA-Z\s]*$')
LNAME_REGEX = re.compile(r'^[a-zA-Z\s]*$')


class UserManager(models.Manager):
    def register_validator(self,postData):
        
        errors = {}
        if not FNAME_REGEX.match(postData['fname']): 
            errors['fname'] = "First name can NOT have numbers or special characters"
        if len(postData['fname']) < 2 or len(postData['lname']) > 25:
            errors['fname'] = "First name should be at least 2 character long"
        if not LNAME_REGEX.match(postData['lname']):
            errors['lname'] = "Last name can NOT have numbers or special characters"
        if len(postData['lname']) < 2 or len(postData['lname']) > 25:
            errors['lname'] = "Last name should be at least 2 character long"
        if not EMAIL_REGEX.match(postData['email']):    
            errors['email'] = "Invalid email address!"
        if len(postData['pass']) < 8:
            errors['pass'] = "Password should be at least 8 character long"
        if postData['pass'] != postData['conf_pass']:
            errors['conf_pass'] = "Password and Password confirmation must match!"
        if len(postData['address']) < 5:
            errors['address'] = "Please enter Valid address"
        if len(postData['city']) < 1:
            errors['city'] = "Please enter City"
        if len(postData['zip_code']) < 1:
            errors['Zip_code'] = "Please enter Zip Code"
        return errors

    def login_validator(self,postData):
        errors = {}
        user = User.objects.filter(email = postData['log_email']) 
        if len(user) < 1:
            errors['log_email'] = "Invalid Credentials"
        else: 
            #if email is found, check the password now
            logged_user = user[0] 
            if not bcrypt.checkpw(postData['log_pass'].encode(), logged_user.password.encode()):
                errors['log_email'] = "Invalid Credentials"
        
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=30)
    isManager = models.BooleanField(default = False)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Service(models.Model):
    service = models.CharField(max_length=250)
    price = models.IntegerField()
    description = models.TextField()
    # date = models.DateField( ("Date"), default=datetime.date.today)

    client = models.ForeignKey(User, related_name="clients", on_delete = models.CASCADE)
    # keeps track of the users who selected a service
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    service = models.ForeignKey(Service, related_name="orders", on_delete = models.CASCADE)
    client = models.ForeignKey(User, related_name="orders", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

