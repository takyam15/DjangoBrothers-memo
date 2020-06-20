from django.forms import ModelForm

from .models import Memo


class MemoForm(ModelForm):
    class Meta:
        model = models.Memo
        fields = ['title', 'slug', 'text']