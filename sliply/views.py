import io
import os

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView

from sliply_project.settings import MEDIA_ROOT
from .forms import UploadForm
from django.core.files.storage import FileSystemStorage

from .tasks import detect_text


class FileUploadView(FormView):
    form_class = UploadForm
    success_url = '/'
    template_name = 'form.html'

    def form_valid(self, form):
        myfile = self.request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        detect_text.delay(filename)
        messages.add_message(self.request, messages.INFO, "OK")
        return redirect('upload')
