from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q

from comments.models import Comentario
from comments.forms import ComentarioForm

from posts.models import Post
from posts.forms import PostForm

from portada.models import Portada

# Create your views here.
def post_list(request):
	registrado=False
	queryset_list = Post.objects.active().order_by("-actualizado")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all().order_by("-actualizado")
		registrado=True

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(titulo__icontains=query)|
				Q(contenido__icontains=query)
				).distinct()

	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	imagen_portada=Portada.objects.first()

	context = {
		"queryset" : queryset,
		"page_request_var": page_request_var,
		"registrado" : registrado,
		"imagen_portada" : imagen_portada
	}
	return render(request,"post_list.html",context)

def post_create(request):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		post_detallado=form.save(commit=False)
		post_detallado.usuario=request.user
		post_detallado.save()
		messages.success(request,"Post creado correctamente")
		return HttpResponseRedirect(reverse("posts:detail", kwargs={"id":post_detallado.id}))

	context = {
		"form" : form,
	}
	return render(request,"post_create_form.html",context)

def post_detail(request,id=None):
	post_detallado = get_object_or_404(Post,id=id)
	registrado = True

	if not request.user.is_staff and not request.user.is_superuser:
		registrado = False

	if post_detallado.fecha_publicacion > timezone.now().date() or post_detallado.borrador:
		if not registrado:
			raise Http404

	comentarios = post_detallado.comentarios

	initial_data = {
		"content_type" : post_detallado.get_content_type,
		"object_id" : post_detallado.id
	}
	comentario_form = ComentarioForm(request.POST or None, initial=initial_data)

	if comentario_form.is_valid():
		c_type = comentario_form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = comentario_form.cleaned_data.get("object_id")
		content_data = comentario_form.cleaned_data.get("contenido")
		parent_obj=None #Por si no hay ninguno, valor por defecto

		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comentario.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment, created = Comentario.objects.get_or_create(
							usuario = request.user,
							content_type= content_type,
							object_id = obj_id,
							contenido = content_data,
							parent = parent_obj
						)
		return HttpResponseRedirect(reverse("posts:detail", kwargs={"id":post_detallado.id}))
	
	context = {
		"post_detallado" : post_detallado,
		"comentarios" : comentarios,
		"registrado" : registrado,
		"comentario_form" : comentario_form
	}
	return render(request,"post_detail.html",context)

def post_update(request,id=None):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404

	post_detallado = get_object_or_404(Post,id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=post_detallado)

	if form.is_valid():
		post_detallado=form.save(commit=False)
		post_detallado.save()
		messages.success(request,"Cambios guardados correctamente")
		return HttpResponseRedirect(reverse("posts:detail", kwargs={"id":post_detallado.id}))

	context = {
		"form" : form,
	}
	return render(request,"post_edit_form.html",context)

def post_delete(request, id=None):
	if not request.user.is_staff and not request.user.is_superuser:
		raise Http404

	post_detallado = get_object_or_404(Post,id=id)
	post_detallado.delete()
	messages.success(request,"Post borrado correctamente")
	return HttpResponseRedirect(reverse("posts:list"))