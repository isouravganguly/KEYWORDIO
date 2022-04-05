from django.db import models
from django.db.models.fields import CharField, NullBooleanField, PositiveIntegerField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class book(models.Model):
    Name= models.CharField(max_length=100)
    subject= models.CharField(max_length=100)
    addedOn= models.DateField()
    Quantity= models.PositiveIntegerField()
    author= models.CharField(max_length=100)

    def __str__(self):
        return self.Name

class librarian(models.Model):
    Name= models.CharField(max_length=40)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True)
    EmpID= models.PositiveBigIntegerField()
    pic=models.ImageField(blank=True, upload_to='profile_image')
    email=models.EmailField( unique=True)
    
    def __str__(self):
        return self.email
        
def create_user_profile(sender,instance, *args, **kwargs):
        if kwargs['created']:
            usern=User.objects.create(username=instance.email, password="dummypass")
            usern.set_password('dummypass')
            
            instance.user=usern
            usern.save()

post_save.connect(create_user_profile, sender=librarian)