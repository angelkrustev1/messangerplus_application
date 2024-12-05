from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from MessangerplusApp.accounts.forms import AppUserCreationForm, AppUserAuthenticationForm, ProfileEditForm, \
    AppUserPasswordChangeForm
from MessangerplusApp.accounts.models import Profile
from MessangerplusApp.common.forms import CommentForm, SearchForm
from MessangerplusApp.posts.models import Post

UserModel = get_user_model()


class AppUserLoginView(LoginView):
    form_class = AppUserAuthenticationForm
    template_name = 'accounts/login-page.html'


def register_page(request):
    form = AppUserCreationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {
        'form': form,
    }

    return render(request, 'accounts/register-page.html', context)


class AppUserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = AppUserPasswordChangeForm
    template_name = 'accounts/change-password-page.html'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.request.user.pk})


@login_required
def profile_details(request, pk):
    profile_user = get_object_or_404(UserModel, pk=pk)
    comment_form = CommentForm()
    all_posts = Post.objects.filter(user__pk=pk)

    context = {
        'profile_user': profile_user,
        'all_posts': all_posts,
        'comment_form': comment_form,
        'can_administer_profiles': request.user.has_perm('accounts.can_administer_profiles'),
        'is_details': False,
    }

    return render(request, 'accounts/profile-details-page.html', context)


@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(Profile, user__pk=pk)

    if not request.user.has_perm('accounts.can_administer_profiles'):
        if request.user != profile.user:
            return redirect('index')

    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('profile-details', pk)

    context = {
        'profile': profile,
        'form': form,
    }

    return render(request, 'accounts/profile-edit-page.html', context)


@login_required
def profile_delete(request, pk):
    profile_user = get_object_or_404(UserModel, pk=pk)

    if not request.user.has_perm('accounts.can_administer_profiles'):
        if request.user != profile_user:
            return redirect('index')

    context = {
        'profile_user': profile_user,
    }

    return render(request, 'accounts/profile-delete-page.html', context)


@login_required
def user_delete(request, pk):
    profile_user = get_object_or_404(UserModel, pk=pk)

    if not request.user.has_perm('accounts.can_administer_profiles'):
        if request.user != profile_user:
            return redirect('index')

        profile_user.delete()
        logout(request)
    else:
        profile_user.delete()
    return redirect('index')


@login_required
def profile_following(request, pk):
    target_user = get_object_or_404(UserModel, pk=pk)
    search_form = SearchForm(request.GET or None)
    following = target_user.profile.following.all()

    if request.method == 'GET':
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            following = following.filter(user__username__icontains=query)

    context = {
        'target_user': target_user,
        'search_form': search_form,
        'following': following,
    }

    return render(request, 'accounts/profile-following-page.html', context)


@login_required
def profile_followers(request, pk):
    target_user = get_object_or_404(UserModel, pk=pk)
    search_form = SearchForm(request.GET or None)
    followers = target_user.profile.followers.all()

    if request.method == 'GET':
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            followers = followers.filter(user__username__icontains=query)

    context = {
        'target_user': target_user,
        'search_form': search_form,
        'followers': followers,
    }

    return render(request, 'accounts/profile-followers-page.html', context)
