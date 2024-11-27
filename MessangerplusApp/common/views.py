from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from MessangerplusApp.common.forms import SearchForm, CommentForm
from MessangerplusApp.common.models import Like, Comment
from MessangerplusApp.posts.models import Post


UserModel = get_user_model()


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'common/no-profile-home-page.html')

    search_form = SearchForm(request.GET or None)
    comment_form = CommentForm()
    all_posts = Post.objects.all()

    if request.method == 'GET':
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            all_posts = all_posts.filter(user__username__icontains=query)

    context = {
        'search_form': search_form,
        'comment_form': comment_form,
        'posts': all_posts,
        'can_administer_posts': request.user.has_perm('can_administer_posts'),
        'is_details': False,
    }

    return render(request, 'common/profile-home-page.html', context)


@login_required
def search_profiles_page(request):
    search_form = SearchForm(request.GET or None)
    all_users = UserModel.objects.filter(~Q(pk=request.user.pk))

    if request.method == 'GET':
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            all_users = all_users.filter(username__icontains=query)

    context = {
        'search_form': search_form,
        'all_users': all_users,
    }

    return render(request, 'common/search-profiles-page.html', context)


@login_required
def comment_functionality(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_post = post
            comment.user = request.user

            comment.save()

        return redirect('post-details', post_pk)


@login_required
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if not request.user.has_perm('can_administer_comments'):
        if request.user != comment.user:
            return redirect('index')

    comment.delete()
    return redirect('post-details', post_pk)


@login_required
def like_functionality(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    liked_object = Like.objects.filter(
        user=request.user,
        to_post=post,
    ).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(user=request.user, to_post=post)
        like.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def follow_functionality(request, user_pk):
    target_user = get_object_or_404(UserModel, pk=user_pk)

    if request.user == target_user:
        return redirect('index')

    target_profile = target_user.profile
    profile = request.user.profile

    is_following = target_profile in profile.following.all()

    if is_following:
        profile.following.remove(target_profile)
    else:
        profile.following.add(target_profile)

    return redirect(request.META.get('HTTP_REFERER'))
