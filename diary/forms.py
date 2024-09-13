from django import forms
from diary.models import Diary
from pytils.translit import slugify


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'content', 'preview']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'preview': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        diary = super().save(commit=False)
        if not diary.slug:
            diary.slug = slugify(diary.title)
        if commit:
            diary.save()
        return diary


class DiaryUpdateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'content', 'preview']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Введите содержание'}),
            'preview': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        diary = super().save(commit=False)
        if not diary.slug:
            diary.slug = slugify(diary.title)
        if commit:
            diary.save()
        return diary
