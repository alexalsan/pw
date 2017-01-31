from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from comments.models import Comentario

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class PostManager(models.Manager):
	def active(self,*args,**kwargs):
		return super(PostManager,self).filter(borrador=False).filter(fecha_publicacion__lte=timezone.now())

# Create your models here.
class Post(models.Model):
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	titulo = models.CharField(max_length=120)
	imagen = models.ImageField(
			upload_to=upload_location, 
			null=True, 
			blank=True, 
			width_field="width_field", 
			height_field="height_field"
			)
	height_field = models.IntegerField(default=0,null=True)
	width_field = models.IntegerField(default=0,null=True)
	contenido = models.TextField()
	borrador = models.BooleanField(default=False)
	fecha_publicacion = models.DateField(auto_now=False,auto_now_add=False)
	publicado = models.DateTimeField(auto_now=False, auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True, auto_now_add=False)
	objects = PostManager()

	def __unicode__(self):
		return self.titulo

	def __str__(self):
		return self.titulo

	class Meta:
		ordering = ["-publicado","-actualizado"]

	@property
	def comentarios(self):
		instance=self
		queryset = Comentario.objects.filtrar_por_instancia(instance)
		return queryset

	@property
	def get_content_type(self):
		instance=self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type