from django.db import models
from django.contrib.auth.models import AbstractUser
from complaints.models import area_master
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .managers  import CustomUserManager
from django.db.models.signals import post_save
from django.utils import timezone


# Create your models here.


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'ADMIN'),
        ('USER','USER'),
        ('FOOD_COLLECTOR', 'FOOD_COLLECTOR'),
    )
    GENDER_CHOICES = (
        ('MALE', 'MALE'),
        ('FEMALE','FEMALE'),
    )
    username = None
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(_("email"), primary_key=True, unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=7, null=False, blank=False, default="MALE")
    role = models.CharField(choices=ROLE_CHOICES, blank=True, default='ADMIN', max_length=20)  # Adjusted max_length
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    USERNAME_FIELD = "email"
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_user = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True,unique=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    area = models.ForeignKey(area_master,to_field='area_name',null=True,blank=True,on_delete=models.PROTECT,related_name="complaint_in_area+")

    profile_image = models.ImageField(null=True, blank=True, upload_to="profile_images/",default="profile_images/default.png")
    

    def __str__(self):
        return self.user.email

class FoodCollectorProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True,unique=True)
    salary = models.CharField(max_length=6,blank=True,null=True)
    area = models.ForeignKey(area_master,to_field='area_name',null=True,blank=True,on_delete=models.PROTECT,related_name="complaint_in_area+")
    profile_image = models.ImageField(null=True, blank=True, upload_to="profile_images/",default="profile_images/default.png")


    def __str__(self):
        return self.user.email
    




@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'USER':
            UserProfile.objects.create(user=instance)
        elif instance.role == 'FOOD_COLLECTOR':
            FoodCollectorProfile.objects.create(user=instance)