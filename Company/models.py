import email
from operator import truediv
from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):
    user=models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    Full_Name=models.CharField(max_length=300, null=True)
    phone1 = models.CharField(max_length=200, null=True)
    phone2 = models.CharField(max_length=200, null=True)
    facebook = models.CharField(max_length=200, null=True,blank=True)
    telegram = models.CharField(max_length=200, null=True,blank=True)
    instagram = models.CharField(max_length=200, null=True,blank=True)
    about = models.TextField(max_length=500, null=True)
    profile_pic=models.ImageField(null=True,blank=True, upload_to='Profile/')
    Company = models.CharField(max_length=200, null=True)
    Job = models.CharField(max_length=200, null=True)
    Country = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return str(self.user)
    
class Region(models.Model):
    Region_Name=models.CharField(max_length=100,blank=True, null=True)
    Location = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    coverArea = models.CharField(max_length=2000,null=True,blank=True)
    def __str__(self) -> str:
        return self.Region_Name
	
class Company_Store(models.Model):
    Store_Name = models.CharField(max_length=200, null=True, unique=True)
    Address = models.CharField(max_length=200, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    def __str__(self) -> str:
        return self.Store_Name
    


class Company_Store_Manager(models.Model):
    user=models.ForeignKey(User,null=True, blank=True,on_delete=models.CASCADE)
    Full_Name=models.CharField(max_length=300, null=True)
    Store=models.OneToOneField(Company_Store,null=True, blank=True,on_delete=models.CASCADE)
    staff=models.CharField(default='Store_Manager',max_length=50)
    profile_pic=models.ImageField(null=True,blank=True, upload_to='Profile/')
    phone = models.CharField(max_length=200, null=True)
    salary = models.FloatField(null=True,blank=True)
    address = models.CharField(max_length=200, null=True)
    about=models.TextField(null=True,blank=True,max_length=500)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    Telegram = models.CharField(max_length=200, null=True)
    facebook = models.CharField(max_length=200, null=True)
    instagram = models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.user)
    
class Product(models.Model):
    Product_Name=models.CharField(max_length=200, null=True)
    img = models.ImageField(null=True,blank=True, upload_to='Product_img/',default='Product_img/castle-beer.jpg')
    Price_in_botle=models.FloatField(null=True,blank=True)
    Price_in_creates=models.FloatField(null=True,blank=True)
    def __str__(self) -> str:
        return self.Product_Name

class Product_Amount_in_Store(models.Model):
    store=models.OneToOneField(Company_Store, null=True, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True, null=True)
    def __str__(self) -> str:
        return str(self.store)

products=Product.objects.all()
for product in products:
    Product_Amount_in_Store.add_to_class(product.Product_Name,models.IntegerField(default=0,null=True,blank=True))  


class Agent(models.Model):
    user=models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    Full_Name=models.CharField(max_length=300, null=True)
    phone1 = models.CharField(max_length=200, null=True)
    phone2 = models.CharField(max_length=200, null=True)
    facebook = models.CharField(max_length=200, null=True)
    telegram = models.CharField(max_length=200, null=True)
    instagram = models.CharField(max_length=200, null=True)
    about = models.TextField(max_length=500, null=True)
    profile_pic=models.ImageField(null=True,blank=True, upload_to='Profile/' ,default="File/Profile/default.png")
    Region=models.ForeignKey(Region,null=True, on_delete=models.CASCADE)
    city = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=500, null=True)
    TIN_NO = models.CharField(max_length=500, null=True)
    License = models.FileField(null=True, blank=True, upload_to='License')
    agreement = models.FileField(null=True, blank=True, upload_to='Agreement')
    marchentId=models.CharField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return str(self.user)
        

class Finance_Manager(models.Model):
    user=models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    Full_Name=models.CharField(max_length=300, null=True)
    phone = models.CharField(max_length=200, null=True)
    staff=models.CharField(default='Finance_manager',max_length=50)
    profile_pic=models.ImageField(null=True,blank=True, upload_to='Profile/')
    salary = models.FloatField(null=True,blank=True)
    address = models.CharField(max_length=200, null=True)
    about=models.TextField(null=True,blank=True,max_length=500)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    telegram = models.CharField(max_length=200, null=True)
    facebook = models.CharField(max_length=200, null=True)
    instagram = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.user.first_name
class Advertisment(models.Model):
    # auther=models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    description=models.TextField(null=True,blank=True,max_length=500)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    product_name= models.CharField(max_length=200, null=True)
    product_price=models.FloatField(default=0.0)
    product_photo=models.ImageField(null=True,blank=True, default='Product_img/new.png',upload_to='Product_img/')

class Agents_message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    email=models.TextField(max_length=200,blank=True,null=True)
    mssg=models.TextField(null=True,blank=True)
    status=models.BooleanField(default=False)

class add_to_store(models.Model):
    Store= models.ForeignKey(Company_Store,null=True, on_delete=models.CASCADE) 
    product = models.CharField(max_length=200, blank=True, null=True)
    qunitiy = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

