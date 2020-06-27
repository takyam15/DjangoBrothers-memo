from django import forms
from django.db.models import Q

from .models import Memo


class MemoForm(forms.ModelForm):
    title = forms.CharField(
        label='タイトル',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'タイトル'
        }),
    )
    slug = forms.CharField(
        label='スラッグ',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'スラッグ'
        })
    )
    text = forms.CharField(
        label='本文',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '本文'
        })
    )

    class Meta:
        model = Memo
        fields = ('title', 'slug', 'text')


class MemoSearchForm(forms.Form):
    keyword = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control mr-sm-2',
            'placeholder': 'メモを検索'
        }),
        required=False,
    )

    def filter_memos(self, memos):
        if self.is_valid():
            keyword = self.cleaned_data.get('keyword')
            if keyword:
                memos = memos.filter(
                    Q(title__icontains=keyword) | Q(text__icontains=keyword)
                )

        return memos