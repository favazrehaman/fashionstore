from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class shopregmodel(models.Model):
    shop_name=models.CharField(max_length=30)
    location=models.CharField(max_length=100)
    idm=models.IntegerField()
    mail=models.EmailField()
    ph=models.IntegerField()
    password=models.CharField(max_length=20)
    def __str__(self):
        return self.shop_name

class productmodel(models.Model):
    shopid=models.IntegerField()
    productname=models.CharField(max_length=30)
    price= models.IntegerField()
    discription=models.CharField(max_length=100)
    image=models.FileField(upload_to='myapp/static')

class profile(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

class cart(models.Model):
    user_id = models.IntegerField()
    productname = models.CharField(max_length=30)
    price = models.IntegerField()
    discription = models.CharField(max_length=100)
    image = models.FileField()
    def __str__(self):
        return self.price

class wishlist(models.Model):
    user_id = models.IntegerField()
    productname = models.CharField(max_length=30)
    price = models.IntegerField()
    discription = models.CharField(max_length=100)
    image = models.FileField()
    def __str__(self):
        return self.price

class buy(models.Model):
    productname = models.CharField(max_length=30)
    price = models.IntegerField()
    discription = models.CharField(max_length=100)
    image = models.FileField()
    quantity=models.IntegerField()

# class customerdetails(models.Model):
#     card_holder_name= models.CharField(max_length=50)
#     card_number= models.IntegerField()
#     date = models.CharField(max_length=50)
#     security_code = models.IntegerField()
class customerdetails1(models.Model):
    card_holder_name= models.CharField(max_length=50)
    card_number= models.IntegerField()
    date = models.CharField(max_length=50)
    security_code = models.IntegerField()

class shopnotification(models.Model):
    content=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)


class usernotification(models.Model):
    content = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)















