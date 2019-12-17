# from __future__ import unicode_literals
from django.db import models

from datetime import date, datetime

import re

class UserManager(models.Manager):
    def basic_validator(self, post_data):    
        errors = {}

        name_regex = re.compile(r'^[a-zA-Z\s]+$')
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not name_regex.match(post_data['first_name']):    # test whether a field matches the pattern            
            errors['first_name'] = "First name must be letters."

        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name not long enough'

        if not name_regex.match(post_data['last_name']):    # test whether a field matches the pattern            
            errors['last_name'] = "Last name must be letters."
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name not long enough'

        if not email_regex.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"

        # try:
        #     user = User.objects.get(email = post_data['email'])
        #     errors['email'] = 'Email is already in use.'
        # except:
        #     pass

        if len(User.objects.filter(email = post_data['email'])) != 0:
            errors['email'] = 'Email is already in use.'

        if len(post_data['password']) < 8 :               
            errors['password_length'] = "Invalid password!"

        if (post_data['password']) != (post_data['confirm_password']) :               
            errors['password_match'] = "Did not confirm password!"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 320)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Shipping_Address(models.Model):
    shipping_address = models.CharField(max_length = 255)
    shipping_city = models.CharField(max_length = 255)
    shipping_zip = models.IntegerField()
    user = models.ForeignKey(User, related_name="shipping_address", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Billing_Address(models.Model):
    billing_address = models.CharField(max_length = 255)
    billing_city = models.CharField(max_length = 255)
    billing_zip = models.IntegerField()
    user = models.ForeignKey(User, related_name="billing_address", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Inventory(models.Model):
    item_brand = models.CharField(max_length = 255)
    item_name = models.CharField(max_length = 255)
    item_primary_color = models.CharField(max_length = 255)
    item_secondary_color = models.CharField(max_length = 255, null=True)
    item_price = models.FloatField(default="50")
    front_img = models.ImageField(upload_to='images/', null=True)
    back_img = models.ImageField(upload_to='images/', null=True)
    top_img = models.ImageField(upload_to='images/', null=True)
    bottom_img = models.ImageField(upload_to='images/', null=True)
    left_img = models.ImageField(upload_to='images/', null=True)
    right_img = models.ImageField(upload_to='images/', null=True)
    condition = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    availability = models.BooleanField()
    buyer = models.ForeignKey(User, related_name="bought", on_delete = models.CASCADE, null=True)
    seller = models.ForeignKey(User, related_name="sold", on_delete = models.CASCADE)

class Shoe(models.Model):
    size = models.FloatField()
    item_sex = models.CharField(max_length = 255)
    item_info = models.ForeignKey(Inventory, related_name="item_type", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






# class Photo(models.Model):
#     inventory_img = models.ImageField(upload_to='images/')
#     Photo = models.ForeignKey(Inventory, related_name="item_photos", on_delete = models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)



