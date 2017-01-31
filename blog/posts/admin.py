from django.contrib import admin

# Register your models here.
from posts.models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["titulo","publicado","actualizado"]
	list_display_links = ["titulo"]
	list_filter = ["publicado","actualizado"]
	search_fields = ["titulo","contenido"]
	class Meta:
		model = Post
			
admin.site.register(Post, PostModelAdmin)