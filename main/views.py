from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import CreateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterForm, ApplicationForm
from .models import Application


def index(request):
    done = Application.objects.filter(status=Application.Status.DONE).order_by('-created_at')[:4]
    in_work_count = Application.objects.filter(status=Application.Status.ACCEPT).count()
    return render(request, 'index.html', {'done_apps': done, 'in_work_count': in_work_count})


class AppLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class RegisterView(FormView ):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'application_form.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = Application.Status.NEW
        messages.success(self.request, 'Заявка создана')
        return super().form_valid(form)


@login_required
def profile(request):
    status = request.GET.get('status', '')
    apps = Application.objects.filter(author=request.user)
    if status in dict(Application.Status.choices):
        apps = apps.filter(status=status)
    return render(request, 'profile.html', {
        'apps': apps,
        'current_status': status,
        'statuses': Application.Status.choices,
    })


class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Application
    template_name = 'application_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return Application.objects.filter(author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status != Application.Status.NEW:
            messages.error(request, 'Нельзя удалить заявку, статус которой изменён')
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect('index')