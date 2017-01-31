from django.db import models
from django.conf import settings

# Create your models here.
class Portada(models.Model):
	imagen = models.ImageField(
			null=True, 
			blank=True, 
			width_field="width_field", 
			height_field="height_field"
			)
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)

	def __unicode__(self):
		return str(self.imagen)

	def __str__(self):
	 	return str(self.imagen)
