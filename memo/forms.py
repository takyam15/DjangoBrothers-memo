from django import forms

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