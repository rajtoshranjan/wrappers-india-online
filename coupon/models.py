from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class CouponCode(models.Model):
	
	code=models.CharField(max_length=12, null=True,unique=True)
	valid_from=models.DateTimeField()
	valid_to=models.DateTimeField()
	discounts=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
	active=models.BooleanField()


	def __str__(self):
		return self.code