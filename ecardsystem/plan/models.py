from django.db import models
from user.models import Student
from django.db.models import JSONField

# Create your models here.



class Plan(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    duration_months = models.PositiveIntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    uid = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    coins = models.PositiveIntegerField(default=0)
    payment_id=models.CharField(default="nopay",max_length=100)
    paid=models.BooleanField(default=False)
    
class UserTimeline(models.Model):
    uid = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    timeline = models.JSONField()

    
   
    




