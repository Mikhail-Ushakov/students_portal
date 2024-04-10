from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, 
                                       PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView,
                                       PasswordResetCompleteView, PasswordResetConfirmView)
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST


from .models import Profile, Subscribe
from .forms import RegistrationForm, EditProfileForm, EditUserForm
# from actions.utils import create_action
# from actions.models import Action

class AccountLoginView(LoginView):
    template_name = 'account/login.html'


class AccountLogoutView(LogoutView):
    template_name = 'account/logout.html'
    

class AccountPassChangeView(PasswordChangeView):
    template_name = 'account/pass_change.html'


class AccountPassChangeDoneView(PasswordChangeDoneView):
    template_name = 'account/pass_change_done.html'


class AccPassResetView(PasswordResetView):
    template_name = 'account/pass_reset.html'
    email_template_name = 'account/pass_reset_email.html'
    success_url = reverse_lazy('pass-reset-done')


class AccPassResetDoneView(PasswordResetDoneView):
    template_name = 'account/pass_reset_done.html'


class AccPassResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/pass_reset_complete.html'

    

class AccPassResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/pass_reset_confirm.html'
    success_url = reverse_lazy('pass-reset-complete')

    


@login_required
def dashboard(request):
    # actions = Action.objects.exclude(user=request.user)
    # following_id = request.user.following.values_list('id', flat=True)
    # if following_id:
    #     actions = actions.filter(user_id__in=following_id)
    # actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    # return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def registr(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            # create_action(new_user, 'create account')
            return render(request, 'account/registration_done.html')
    else:
        form = RegistrationForm()
    return render(request, 'account/registration.html', {'form': form})    

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditUserForm(instance=request.user, data=request.POST)
        profile_form = EditProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect(reverse('dashboard'))
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
    return render(request, 'account/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def users_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/users_list.html', {'users': users})

@login_required
def user_detail(request, user_name):
    select_user = User.objects.filter(username=user_name, is_active=True)[0] #лучше get object or 404 использовать 
    if select_user == request.user:
        return HttpResponseRedirect(reverse('dashboard'))
    return render(request, 'account/user_detail.html', {'select_user': select_user})


@require_POST
@login_required
def subscribe(request, user_id, action):
    user_to = get_object_or_404(User, id=user_id)
    if action == 'follow':
        Subscribe.objects.get_or_create(user_from=request.user, user_to=user_to)
        # create_action(request.user, 'is following', user_to)
    elif action == 'unfollow':
        Subscribe.objects.filter(user_from=request.user, user_to=user_to).delete()
    
    return HttpResponseRedirect(reverse('user-detail', args=[user_to.username]))