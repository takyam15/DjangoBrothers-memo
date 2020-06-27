from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView,
)

from .forms import MemoForm, MemoSearchForm
from .models import Memo


# Create your views here.

class MemoList(ListView):
    model = Memo
    template_name = 'memo/index.html'
    paginate_by = 10

    def get_queryset(self):
        form = MemoSearchForm(self.request.GET)
        queryset = super().get_queryset()
        queryset = form.filter_memos(queryset)
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context['search_form'] = MemoSearchForm(self.request.GET)
        return context


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
