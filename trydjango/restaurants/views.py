from django.db.models import Q
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import RestaurantLocationCreateForm
from .models import RestaurantLocation

def restaurant_createview(request):
	form = RestaurantLocationCreateForm(request.POST or None)
	errors = None
	if form.is_valid():
		# customization!
		# This place is signal works! Like a pre_save
		form.save()
		# Like a post_save
		return HttpResponseRedirect('/restaurants/')
		
	if form.errors:
		print(form.errors)
		errors = form.errors

	template_name = 'restaurants/form.html'
	context = {'form': form}
	return render(request, template_name, context)

def restaurant_listview(request):
	template_name = 'restaurants/restaurants_list.html'
	queryset = RestaurantLocation.objects.all()
	context = {
		"object_list": queryset
	}
	return render(request, template_name, context)

def restaurant_detailview(request, pk):
	template_name = 'restaurants/restaurantlocation_detail.html'
	obj = RestaurantLocation.objects.get(slug = slug)
	context = {
		"object": obj
	}
	return render(request, template_name, context)


class RestaurantListView(ListView):
	template_name = 'restaurants/restaurants_list.html'

	def get_queryset(self):
		print(self.kwargs)
		slug = self.kwargs.get("slug")
		if slug:
			queryset = RestaurantLocation.objects.filter(Q(category__iexact=slug) | Q(category__contains=slug))
		else:
			queryset = RestaurantLocation.objects.all()
		return queryset	

class RestaurantDetailView(DetailView):
	queryset = RestaurantLocation.objects.all() #filter(category__iexact='asian')

	# def get_object(self, *args, **kwargs):
	# 	slug = self.kwargs.get('slug')
	# 	obj = get_object_or_404(RestaurantLocation, slug=slug) # pk = rest_id
	# 	return obj

class RestaurantCreateView(CreateView):
	form_class = RestaurantLocationCreateForm
	template_name = 'restaurants/form.html'

	success_url = '/restaurants/'