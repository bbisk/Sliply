
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.db.models.query_utils import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from sliply_project.settings import MEDIA_URL
from .models import Slip, Item
from .tasks import parse_text
from .forms import UploadForm, SlipCreateForm, ItemCreateForm

from .tasks import detect_text


#Slip views

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

        # messages.add_message(self.request, messages.INFO, "OK")
        return redirect('slips')

class SlipListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        queryset = Slip.objects.filter(owner=self.request.user).order_by('-create_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        total_amount = queryset.aggregate(Sum('total_amount'))
        context['total_amount_sum'] = total_amount['total_amount__sum']
        return context



class SlipDetailView(LoginRequiredMixin, DetailView):
    queryset = Slip.objects.all()

    def get_context_data(self, **kwargs):
        get_action = self.request.GET.get('action')
        if get_action == 'rescan':
            parse_text.delay(self.object.raw_text, self.object.pk, get_action)
            messages.add_message(self.request, messages.INFO, "Processing text detection...")
        context = super().get_context_data(**kwargs)
        context['path'] = MEDIA_URL
        return context


class SlipUpdateView(LoginRequiredMixin, UpdateView):
    model = Slip
    fields = ('purchase_date', 'seller_name', 'total_amount', 'payment_type', 'raw_text')


class SlipDeleteView(LoginRequiredMixin, DeleteView):
    model = Slip
    success_url = reverse_lazy('slips')


class SearchView(SlipListView):
    def get_queryset(self):
        query = self.request.GET.get('query', default="")
        fromto = self.request.GET.get('fromto', default="")
        fromdate = self.request.GET.get('from', default="")
        todate = self.request.GET.get('to', default="")

        queryset = Slip.objects.filter(owner=self.request.user).order_by('-create_date').filter(seller_name__icontains=query) or \
                   Slip.objects.filter(owner=self.request.user).order_by('-create_date').filter(item__item_name__icontains=query)
        if fromto == "from" and fromdate != "" and todate!="":
            queryset = queryset.filter(Q(purchase_date__gte=fromdate)& Q(purchase_date__lte=todate))

        if fromto == "from" and fromdate != "" and todate == "":
            queryset = queryset.filter(purchase_date=fromdate)

        if fromto == "date" and fromdate != "":
            queryset = queryset.filter(purchase_date=fromdate)

        return queryset

class SlipCreateView(LoginRequiredMixin, CreateView):
        form_class = SlipCreateForm
        template_name = 'form.html'

        def form_valid(self, form):
            form_to_save = form.save(commit=False)
            form_to_save.owner = self.request.user
            form_to_save.save()
            return redirect('slips')


#Item views

class ItemListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        query = self.request.GET.get('query', default="")
        fromto = self.request.GET.get('fromto', default="")
        fromdate = self.request.GET.get('from', default="")
        todate = self.request.GET.get('to', default="")

        queryset = Item.objects.filter(owner=self.request.user).order_by('-create_date').filter(slip__seller_name__icontains=query) or \
                   Item.objects.filter(owner=self.request.user).order_by('-create_date').filter(item__icontains=query)
        if fromto == "from" and fromdate != "" and todate!="":
            queryset = queryset.filter(Q(slip__purchase_date__gte=fromdate)& Q(slip__purchase_date__lte=todate))

        if fromto == "from" and fromdate != "" and todate == "":
            queryset = queryset.filter(slip__purchase_date=fromdate)

        if fromto == "date" and fromdate != "":
            queryset = queryset.filter(slip__purchase_date=fromdate)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        total_amount = queryset.aggregate(Sum('price'))
        context['total_amount_sum'] = total_amount['price__sum']
        return context

class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'sliply/slip_form.html'
    fields = ('item_name', 'quantity', 'price', 'raw_text')


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'sliply/slip_confirm_delete.html'
    success_url = reverse_lazy('items')


class ItemCreateView(LoginRequiredMixin, CreateView):
    form_class = ItemCreateForm
    template_name = 'form.html'

    def form_valid(self, form):
        form_to_save = form.save(commit=False)
        form_to_save.owner = self.request.user
        form_to_save.save()
        return redirect('items')

#User views

class UserProfileView(LoginRequiredMixin, DetailView):

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')