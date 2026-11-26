from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import CreateView, DeleteView, FormView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import RegisterForm, ApplicationForm, AcceptForm, DoneForm
from .models import Application


def index(request):
    done = Application.objects.filter(status=Application.Status.DONE).order_by('-created_at')[:4]
    in_work_count = Application.objects.filter(status=Application.Status.ACCEPT).count()
    return render(request, 'index.html', {'done_apps': done, 'in_work_count': in_work_count})


class AppLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class RegisterView(FormView):
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
    if request.user.is_staff:
        apps = Application.objects.all()
    else:
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


class StaffRequiredMixin(UserPassesTestMixin):
    login_url = '/login/'
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class AdminDashboard(StaffRequiredMixin, View):
    model = Application
    template_name = 'superadmin/dashboard.html'
    context_object_name = 'apps'

class AcceptApplicationView(StaffRequiredMixin, View):
    form_class = ApplicationForm
    def get(self, request, pk):
        app = get_object_or_404(Application, pk=pk)
        if app.status != Application.Status.NEW:
            return redirect('admin_dashboard')
        return render(request, 'superadmin/accept_form.html')
    def post(self, request, pk):
        app = get_object_or_404(Application, pk=pk)
        if app.status != Application.Status.NEW:
            return redirect('admin_dashboard')

        form = AcceptForm(request.POST)
        if form.is_valid():
            app.status = Application.Status.ACCEPT
            app.admin_comment = form.cleaned_data['comment']
            app.save()
            return redirect('admin_dashboard')
        return render(request, 'superadmin/accept_form.html', {'form': form, 'app': app})

class DoneApplicationView(StaffRequiredMixin, View):
    form_class = DoneForm
    def get(self, request, pk):
        app = get_object_or_404(Application, pk=pk)
        if app.status != Application.Status.NEW:
            return redirect('admin_dashboard')
        return render(request, 'superadmin/done_form.html', {'form': DoneForm(), 'app': app})

    def post(self, request, pk):
        app = get_object_or_404(Application, pk=pk)
        if app.status != Application.Status.NEW:
            return redirect('admin_dashboard')

        form = DoneForm(request.POST, request.FILES)
        if form.is_valid():
            app.status = Application.Status.DONE
            app.design_image = form.cleaned_data['design_image']
            app.save()
            return redirect('admin_dashboard')
        return render(request, 'superadmin/done_form.html', {'form': form, 'app': app})