from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from MessangerplusApp.accounts.models import Profile
from MessangerplusApp.chats.forms import MessageForm
from MessangerplusApp.chats.models import Message
from MessangerplusApp.chats.serializers import MessageSerializer
from MessangerplusApp.common.forms import SearchForm


UserModel = get_user_model()


@login_required
def chats_page(request):
    search_form = SearchForm(request.GET or None)
    profile = request.user.profile

    following_users = profile.following.all()
    mutual_followers = following_users.filter(following=profile)

    if request.method == 'GET':
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            mutual_followers = mutual_followers.filter(user__username__icontains=query)

    context = {
        'search_form': search_form,
        'mutual_followers': mutual_followers,
    }

    return render(request, 'chats/all-chats-page.html', context)


@login_required
def chat_one_on_one(request, pk):
    target_user = get_object_or_404(UserModel, pk=pk)
    profile = request.user.profile

    if target_user.profile not in profile.following.all() or profile not in target_user.profile.following.all():
        return redirect('chats')

    message_form = MessageForm(request.POST or None)

    if request.method == 'POST':
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.sender = request.user
            message.recipient = target_user
            message.save()

            return redirect('chat-one-on-one', pk)

    shared_messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=target_user) | Q(sender=target_user) & Q(recipient=request.user))
    ).order_by('-publication_datetime')

    context = {
        'target_user': target_user,
        'message_form': message_form,
        'shared_messages': shared_messages,
        'can_administer_messages': request.user.has_perm('chats.can_administer_messages'),
    }

    return render(request, 'chats/one-on-one-chat-page.html', context)


@login_required
def message_delete(request, pk, message_pk):
    message = get_object_or_404(Message, pk=message_pk)

    if not request.user.has_perm('can_administer_messages'):
        if message.sender != request.user:
            return redirect('index')

    message.delete()
    return redirect('chat-one-on-one', pk)


class MessagesBetweenUsersView(APIView):
    def get(self, request, sender_pk, recipient_pk):
        target_user = UserModel.objects.get(pk=recipient_pk)
        profile = request.user.profile

        shared_messages = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=target_user) | Q(sender=target_user) & Q(recipient=request.user))
        )

        shared_messages_json = MessageSerializer(shared_messages, many=True)

        return Response(shared_messages_json.data)


