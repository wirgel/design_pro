import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from .models import Application, Category

CYRILLIC_RE = re.compile(r"^[А-Яа-яЁё\-\s]+$")
LOGIN_RE = re.compile(r"^[a-zA-Z\-]+$")
MAX_IMAGE_SIZE = 2 * 1024 * 1024


class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True, label="ФИО")
    username = forms.CharField(max_length=100, label="Логин", required=True)
    email = forms.EmailField(label='E-mail', required=True)
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput, required=True)
    consent = forms.BooleanField(
        label='Согласен на обработку персональных данных',
        error_messages={'required': 'Необходимо согласие на обработку ПД'}
    )

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name'].strip()
        if not CYRILLIC_RE.match(full_name):
            raise ValidationError('ФИО: только кириллица, дефис и пробел')
        return full_name

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if not LOGIN_RE.match(username):
            raise ValidationError('Логин: только латиница и дефис')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Этот логин занят")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Этот email уже используется')
        return email

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Пароли не совпадают')
        return cd

    def save(self):
        full_name = self.cleaned_data['full_name'].split()
        first_name = full_name[0] if full_name else ''
        last_name = ' '.join(full_name[1:]) if len(full_name) > 1 else ''
        return User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=first_name,
            last_name=last_name,
        )


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'content', 'category', 'image']

    def clean_image(self):
        img = self.cleaned_data['image']
        if img.size > MAX_IMAGE_SIZE:
            raise forms.ValidationError('Размер файла не должен превышать 2 Мб.')
        return img


class AcceptForm(forms.Form):
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea)


class DoneForm(forms.Form):
    design_image = forms.ImageField(
        label='Изображение дизайна',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'bmp'])],
    )

    def clean_design_image(self):
        img = self.cleaned_data['design_image']
        if img.size > MAX_IMAGE_SIZE:
            raise forms.ValidationError('Размер файла не должен превышать 2 Мб.')
        return img


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']