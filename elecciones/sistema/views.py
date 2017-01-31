from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from sistema.forms import MesaForm
from sistema.models import Partido,Mesa,Circunscripcion,Resultado
#from sistema.forms import ComentarioForm

# Create your views here.
def sistema_list(request):
	return render(request,"index.html",{})

def is_supervisor(user):
	return user.is_superuser

class CircList(ListView):
	template_name = 'circ_list.html'
	model = Circunscripcion

class CircDetail (DetailView):
	template_name = 'circ_detail.html'
	model = Circunscripcion

	#def get_context_data(self, **kwargs):
	#	context = super(CircDetail, self).get_context_data(**kwargs)
	#	return context

class CircCreate(CreateView):
	template_name = 'circ_create.html'
	model = Circunscripcion
	fields = ['nombre','num_esc']

	@method_decorator(login_required)
	@method_decorator(user_passes_test(is_supervisor))
	def dispatch(self, request, *args, **kwargs):
		return super(CircCreate, self).dispatch(request, *args, **kwargs)

class CircDelete(DeleteView):
	template_name = 'circ_delete.html'
	model = Circunscripcion
	success_url = reverse_lazy('sistema:circ_list')

	@method_decorator(login_required)
	@method_decorator(user_passes_test(is_supervisor))
	def dispatch(self, request, *args, **kwargs):
		return super(CircDelete, self).dispatch(request, *args, **kwargs)

class CircUpdate(UpdateView):
	template_name = 'circ_update.html'
	model = Circunscripcion
	fields = ['nombre', 'num_esc']

	@method_decorator(login_required)
	@method_decorator(user_passes_test(is_supervisor))
	def dispatch(self, request, *args, **kwargs):
		return super(CircUpdate, self).dispatch(request, *args, **kwargs)

def mesa_list(request, id=None):
	circ = get_object_or_404(Circunscripcion,id=id)
	queryset = circ.mesa_set.all()
	context = {
		"circ" : circ,
		"queryset" : queryset,
	}
	return render(request,"mesa_list.html",context)

def mesa_detail(request, id=None):
	mesa = get_object_or_404(Mesa,id=id)
	context = {
		"mesa" : mesa,
	}
	return render(request,"mesa_detail.html",context)

@login_required
@user_passes_test(is_supervisor)
def mesa_create(request,id=None):
	circ = get_object_or_404 (Circunscripcion, id=id)
	form = MesaForm(request.POST or None)

	if form.is_valid():
		mesa=form.save(commit=False)
		mesa.circunscripcion=circ
		mesa.save()
		messages.success(request,"Mesa creada correctamente")
		return HttpResponseRedirect(reverse("sistema:mesa_list", kwargs={"id":id}))

	context = {
		"form" : form,
	}
	
	return render(request,"mesa_create.html",context)

@login_required
@user_passes_test(is_supervisor)
def mesa_update(request,id=None):
	mesa = get_object_or_404(Mesa,id=id)
	form = MesaForm(request.POST or None, instance=mesa)

	if form.is_valid():
		mesa=form.save(commit=False)
		mesa.save()
		messages.success(request,"Cambios guardados correctamente")
		return HttpResponseRedirect(reverse("sistema:mesa_list", kwargs={"id":mesa.circunscripcion.id}))

	context = {
		"form" : form,
	}
	return render(request,"mesa_update.html",context)