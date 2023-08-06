from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.http import HttpResponseRedirect, HttpResponse
from .models import Photo
from .forms import PhotoForm

class MainHomeView(ListView):
    model = Photo
    template_name = "ex00/main.html"
    form_class=PhotoForm
    queryset = Photo.objects.all()
    context_object_name='photo_list'

    def get_queryset(self):
            return Photo.objects.all()

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['photo_list'] = Photo.objects.all()
        context['form'] = PhotoForm()
        return context

    def form_valid(self, form: PhotoForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)

    def post(self, request):
        self.object_list = self.get_queryset()
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                print("e",e)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


    