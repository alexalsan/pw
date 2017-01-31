from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ComentarioManager (models.Manager):
	def all(self):
		qs = super(ComentarioManager,self).filter(parent=None)
		return qs

	def filtrar_por_instancia(self,instancia):
		content_type = ContentType.objects.get_for_model(instancia.__class__)
		obj_id = instancia.id
		queryset = super(ComentarioManager,self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
		return queryset

# Create your models here.
class Comentario(models.Model):
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = GenericForeignKey('content_type', 'object_id')
	parent = models.ForeignKey("self",null=True,blank=True)

	contenido = models.TextField()
	publicado = models.DateTimeField(auto_now_add=True)
	objects = ComentarioManager()

	def __unicode__(self):
		return str(self.usuario.username)

	def __str__(self):
		return str(self.usuario.username)

	class Meta:
		ordering = ["-publicado"]

	def children(self):
		return Comentario.objects.filter(parent=self)
	
	@property
	def is_parent(self): #para ver si es un comentario padre o hijo
		if self.parent is not None:
			return False
		return True