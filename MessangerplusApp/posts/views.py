from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from MessangerplusApp.common.forms import SearchForm, CommentForm
from MessangerplusApp.common.models import Comment, Like
from MessangerplusApp.posts.forms import PostCreationForm, PostEditForm
from MessangerplusApp.posts.models import Post


UserModel = get_user_model()


@login_required
def posts_for_you_page(request):
    search_form = SearchForm(request.GET or None)
    comment_form = CommentForm()

    profile = request.user.profile
    followed_profiles = profile.following.all()
    all_posts = Post.objects.filter(user__profile__in=followed_profiles)

    if request.method == 'GET':
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            all_posts = all_posts.filter(user__username__icontains=query)

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    context = {
        'search_form': search_form,
        'comment_form': comment_form,
        'posts': posts_page,
        'can_administer_posts': request.user.has_perm('can_administer_posts'),
    }

    return render(request, 'common/profile-home-page.html', context)


@login_required
def create_post(request):
    form = PostCreationForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')

    context = {
        'form': form,
    }

    return render(request, 'posts/post-create-page.html', context)


@login_required
def post_details(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = Comment.objects.filter(to_post__pk=post_pk)
    comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'can_administer_posts': request.user.has_perm('can_administer_posts'),
        'can_administer_comments': request.user.has_perm('can_administer_comments'),
        'is_details': True,
    }

    return render(request, 'posts/post-details-page.html', context)


@login_required
def post_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if not request.user.has_perm('posts.can_administer_posts'):
        if request.user != post.user:
            return redirect('index')

    form = PostEditForm(request.POST or None, instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('post-details', post_pk)

    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'posts/post-edit-page.html', context)


@login_required
def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if not request.user.has_perm('posts.can_administer_posts'):
        if request.user != post.user:
            return redirect('index')

    post.delete()
    return redirect('profile-details', post.user.pk)
