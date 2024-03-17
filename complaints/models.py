from django.db import models

# Create your models here.

class area_master(models.Model):
    status_id_choices = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )
    area_id = models.AutoField(primary_key=True,unique=True)
    area_name = models.CharField(max_length=150,null=False,blank=False,unique=True)
    status_id = models.CharField(max_length=9,null=False,blank=False,choices=status_id_choices,default='active')

    def __str__(self):
        return self.area_name
    
    class Meta:
        verbose_name_plural = "Areas"


class FoodCollectionRequests(models.Model):
    status_choices = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    )
    complaint_id = models.AutoField(primary_key=True,null=False,blank=False,unique=True)
    complainant_name = models.CharField(max_length=150,null=False,blank=False)
    complainant_contact_no = models.IntegerField(null=False, blank=False)
    complainant_email = models.EmailField(null=False, blank=False)
    area = models.ForeignKey(area_master,to_field='area_name',null=True,blank=True,on_delete=models.PROTECT,related_name="complaint_in_area+")
    complainant_address = models.TextField(max_length=1000,null=False,blank=False)
    detailed_description = models.TextField(max_length=10000,null=False,blank=False)
    status = models.CharField(choices=status_choices, max_length=10,null=True, blank=True, default='Pending')
    changed_by = models.CharField(max_length=100000,null=True,blank=True, default=" ")


    def __str__(self):
        return self.complainant_email
    
    class Meta:
        verbose_name_plural = "FoodCollectionRequests"


class feedbacks_master_byUsers(models.Model):
    announcement_id = models.AutoField(primary_key=True,unique=True)
    title = models.CharField(max_length=50,blank=False,null=False)
    description = models.TextField(max_length=5000,blank=False,null=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Feedbacks by Users"

class feedbacks_master_byFC(models.Model):
    announcement_id = models.AutoField(primary_key=True,unique=True)
    title = models.CharField(max_length=50,blank=False,null=False)
    description = models.TextField(max_length=5000,blank=False,null=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Feedbacks by Food Collector"