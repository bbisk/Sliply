
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView

from sliply.models import Slip
from sliply.tasks import parse_text
from .forms import UploadForm
from django.core.files.storage import FileSystemStorage

from .tasks import detect_text


class FileUploadView(LoginRequiredMixin, CreateView):
    form_class = UploadForm
    template_name = 'form.html'

    def form_valid(self, form):
        files = self.request.FILES.getlist('scanfile')
        for n in range(0, len(files)):
            filename = files[n]
            owner = self.request.user
            save_to_db = Slip.objects.create(owner=owner, scanfile=filename)
            detect_text.delay(filename.name, save_to_db.pk)

            # form_to_save = form.save(commit=False)
            # form_to_save.scanfile = files[n]
            # form.save()
        # filename = form_to_save.scanfile.name
        # pk = form_to_save.id
        # myfile = self.request.FILES['file']
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # detect_text.delay(filename, pk)
        messages.add_message(self.request, messages.INFO, "OK")
        return redirect('upload')

class SlipListView(ListView):
    # template_name = CONTACTS_VIEW_TEMPLATE
    def get_queryset(self):
        queryset = Slip.objects.filter(owner=self.request.user).order_by('create_date')
        return queryset


class SlipDetailView(DetailView):
    queryset = Slip.objects.all()

    def get_context_data(self, **kwargs):
        if self.request.GET.get('action') == 'rescan':
            parse_text.delay(self.object.raw_text, self.object.pk)
        context = super().get_context_data(**kwargs)
        return context



    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['path'] = MEDIA_URL
    #     return context

class SlipUpdateView(UpdateView):
    model = Slip
    fields = ('purchase_date', 'seller_name', 'total_amount', 'raw_text')
