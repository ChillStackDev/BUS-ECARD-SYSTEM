from django.db import models
from django.contrib.auth.models import User
import hashlib
# Create your models here.




class Student(models.Model):
    image = models.ImageField(upload_to='', blank=True, null=True, default='dp.png') 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sscBoard=models.CharField(blank=True,max_length=100)
    sscPass=models.CharField(blank=True,max_length=6)
    sscHNO=models.CharField(blank=True,max_length=15)
    father_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15)
    aadhar_number = models.CharField(max_length=12)
    district = models.CharField(max_length=100)
    mandal = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building_number = models.CharField(max_length=15)
    college_name = models.CharField(max_length=100)
    coursename=models.CharField(blank=True,max_length=20)
    college_id = models.CharField(max_length=20)
    route_details = models.TextField()
    uid = models.CharField(max_length=15, blank=True, unique=True)
    card_id=models.CharField(max_length=15, blank=True, unique=True)
    verified = models.BooleanField(default=False)
    data_integrity_hash = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):
        
        critical_data = (
            self.sscBoard + 
            self.sscPass + 
            self.sscHNO + 
            self.father_name + 
            self.gender + 
            str(self.date_of_birth) + 
            self.mobile_number + 
            self.aadhar_number + 
            self.district + 
            self.mandal + 
            self.street + 
            self.building_number + 
            self.college_name + 
            self.coursename + 
            self.college_id + 
            self.route_details
        )

        
        hash_value = hashlib.sha256(critical_data.encode()).hexdigest()

       
        self.data_integrity_hash = hash_value

       
        super().save(*args, **kwargs)

    def verify_data_integrity(self):
        
        critical_data = (
            self.sscBoard + 
            self.sscPass + 
            self.sscHNO + 
            self.father_name + 
            self.gender + 
            str(self.date_of_birth) + 
            self.mobile_number + 
            self.aadhar_number + 
            self.district + 
            self.mandal + 
            self.street + 
            self.building_number + 
            self.college_name + 
            self.coursename + 
            self.college_id + 
            self.route_details
        )

        recalculated_hash = hashlib.sha256(critical_data.encode()).hexdigest()

        return recalculated_hash == self.data_integrity_hash

    def __str__(self):
        return str(self.uid)


