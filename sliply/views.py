
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView

from sliply.models import Slip
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
