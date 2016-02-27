from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class Company:
	name = models.CharField(max_length=100)
	#More fields will be needed...

class Department:
	company_rel = models.ForeignKey(Company,on_delete=models.CASCADE )
	name = models.CharField(max_length=100)
	#logo = pending....
	#color  = if needed....

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE )
