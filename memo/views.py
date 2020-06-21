from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView,
)

from .forms import MemoForm
from .models import Memo


# Create your views here.

class MemoList(ListView):
    model = Memo
    template_name = 'memo/index.html'


class MemoDetail(DetailView):
    model = Memo
    template_name = 'memo/detail.html'


class MemoCreate(CreateView):
    model = Memo
    form_class = MemoForm
    template_name = 'memo/new.html'
    success_url = reverse_lazy('memo:index')


class MemoDelete(DeleteView):
    model = Memo
    template_name = 'memo/delete.html'
    success_url = reverse_lazy('memo:index')


class MemoUpdate(UpdateView):
    model = Memo
    form_class = MemoForm
    template_name = 'memo/edit.html'
    
    def get_success_url(self):
        return resolve_url('memo:detail', slug=self.kwargs['slug'])
