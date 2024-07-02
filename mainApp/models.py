from datetime import timedelta
from django.utils import timezone
from django.db import models

class Bank(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    baseprice = models.IntegerField()
    term = models.IntegerField()
    income = models.FloatField(max_length=20)
    earning = models.FloatField(max_length=20)
    totalrevenue = models.FloatField(max_length=20,default=0)
    totalyield = models.FloatField(max_length=20)
    description = models.TextField()
    purchaselimit = models.IntegerField()
    desc1 = models.CharField(max_length=100,null=True,blank=True)
    desc2 = models.CharField(max_length=100,null=True,blank=True)
    desc3 = models.CharField(max_length=100,null=True,blank=True)
    desc4 = models.CharField(max_length=100,null=True,blank=True)
    desc5 = models.CharField(max_length=100,null=True,blank=True)
    stock = models.CharField(max_length=20,default="In Stock")
    pic1 = models.ImageField(upload_to="images",default="noimagep.jpg",null=True,blank=True)
    pic2 = models.ImageField(upload_to="images",default="noimagep.jpg",null=True,blank=True)
    pic3 = models.ImageField(upload_to="images",default="noimagep.jpg",null=True,blank=True)

    def __str__(self):
        return self.name

class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    name = models.CharField(max_length=200,default="")
    account = models.IntegerField(default=0)
    totalamount = models.IntegerField(default=0)
    referral = models.CharField(max_length=100,default="",unique=True)
    rech = models.IntegerField(default=0)
    product = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    dailyincome = models.IntegerField(default=0)
    ifsc = models.CharField(max_length=200,default="")
    bank = models.CharField(max_length=200,default="")
    password = models.CharField(max_length=200,default="")

    def __str__(self):
        return self.phone

payment = ((1,'Pending'),(2,'Done'))
class Withdrawn(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,default="")
    account = models.IntegerField(default=0)
    ifsc = models.CharField(max_length=200,default="")
    bank = models.CharField(max_length=200,default="")
    amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=payment,default=1)


    def __str__(self):
        return str(self.id)
    
class Buy(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    wallet = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    last_clicked = models.DateTimeField(null=True, blank=True)

    def can_click(self):
        if not self.last_clicked:
            return True
        return timezone.now() > self.last_clicked + timedelta(hours=24)

    def __str__(self):
        return f'{self.buyer.phone} Profile'
    
class Reff(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.CharField(max_length=200,default="")
    invite = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    
class Recharge(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    
    
