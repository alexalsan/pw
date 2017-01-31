from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
#from django.contrib.contenttypes.fields import GenericForeignKey
#from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Partido (models.Model):
	nombre=models.CharField(max_length=100,unique=True)

	def __unicode__(self):
		return self.nombre

	def __str__(self):
		return self.nombre

class Circunscripcion (models.Model):
	nombre=models.CharField(max_length=100)
	num_esc=models.IntegerField() #núm de escaños a repartir

	def get_absolute_url(self):
		return reverse("sistema:circ_detail", kwargs={"pk": self.pk})

	def __unicode__(self):
		return self.nombre

	def __str__(self):
		return self.nombre

class Mesa (models.Model):
	nombre=models.CharField(max_length=100)
	circunscripcion=models.ForeignKey('Circunscripcion')

	def __unicode__(self):
		return self.nombre

	def __str__(self):
		return self.nombre

class Resultado (models.Model):
	votos=models.PositiveIntegerField() #núm de votos en cada mesa
	partido=models.ForeignKey('Partido')
	mesa=models.ForeignKey('Mesa')

	def __unicode__(self):
		return self.nombre

	def __str__(self):
		return self.nombre