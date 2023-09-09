from django.db import models

class UserCompMaster(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=30)
    contact=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    userfirst=models.BooleanField(default=1)
    isadmin = models.BooleanField(default=0)
    
    companyname=models.CharField(max_length=20,null=True)
    address=models.CharField(max_length=100,null=True)
    pincode=models.CharField(max_length=10,null=True)
    state=models.CharField(max_length=20,null=True)
    city=models.CharField(max_length=20,null=True)
    gstin=models.CharField(max_length=20,null=True)
    
class CategoryMaster(models.Model):
    catname=models.CharField(max_length=20)
    active=models.CharField(max_length=5)
    #gstinid=models.CharField(max_length=10)#for addressing differenrt individual company/users

class SubCatMaster(models.Model):
    catname=models.CharField(max_length=20)
    subcat=models.CharField(max_length=20)
    active=models.CharField(max_length=3)
    #gstinid=models.CharField(max_length=10)

class UOMMaster(models.Model):
    uomname=models.CharField(max_length=10)
    active=models.CharField(max_length=4)
    #gstinid=models.CharField(max_length=10)

class ProductMaster(models.Model):
    prodcat=models.CharField(max_length=20) #product category
    subcat=models.CharField(max_length=20) #sub category of product
    prodname=models.CharField(max_length=20) # product name
    mainuom=models.CharField(max_length=20) #main unit of measure
    salesuom=models.CharField(max_length=20) # sales unit of measure
    contains=models.CharField(max_length=20)
    purchaserate=models.CharField(max_length=20) # purchase rate or bought price
    salesrate=models.CharField(max_length=20) # selling price
    stock=models.CharField(max_length=20) # available stock
    warnstock=models.CharField(max_length=20) #warning stock
    discount=models.CharField(max_length=20) #discount
    tax=models.CharField(max_length=20) #tax for aitem
    hsncode=models.CharField(max_length=20)#HSN unique code for product


class BillingMaster(models.Model):
    custname= models.CharField(max_length=20) #customer name
    custcontact=models.CharField(max_length=20)#customer contact number
    custaddress=models.CharField(max_length=20)#customer address
    cashspend=models.CharField(max_length=20) #total amount spend of customer
    prodbought=models.CharField(max_length=500) #list of product in one column
    profitsininr=models.CharField(max_length=20,null=True) #profit in indian rupees

class DefCatSubcat(models.Model):
    catname = models.CharField(max_length=20)
    subcat = models.CharField(max_length=500)