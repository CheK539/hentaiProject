from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from rest_framework import generics

from .forms import HentaiForm
from .models import Hentai
from .serializer import HentaiListSerializer, HentaiSerializer


class JsonList(generics.ListCreateAPIView):
    queryset = Hentai.objects.all()
    serializer_class = HentaiListSerializer


class CurrentJson(generics.ListCreateAPIView):
    serializer_class = HentaiSerializer
    model = Hentai

    def get_queryset(self):
        return self.model.objects.filter(title=self.kwargs['title'])


class HentaiListPage(ListView):
    template_name = 'hentai_information/hentai_list_page.html'
    model = Hentai

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

        return redirect('authentication:login')


class AddHentaiPage(CreateView):
    template_name = 'hentai_information/add_hentai_page.html'
    model = Hentai
    form_class = HentaiForm
    success_url = reverse_lazy('hentai_information:hentaiListPage')


class HentaiInformationPage(TemplateView):
    template_name = 'hentai_information/hentai_information.html'

    def get_context_data(self, **kwargs):
        title = 'title'
        hentai = None
        parameters = self.request.GET

        if title in parameters and parameters[title]:
            hentai = Hentai.objects.filter(title=parameters[title]).first()

        context = super().get_context_data(**kwargs)
        context['hentai'] = hentai
        return context
