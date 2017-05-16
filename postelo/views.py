from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm
from .models import Message


def message_index(request):
    messages = Message.objects.all().filter(recipient=request.user).filter(draft=False).filter(is_trash=False)\
        .order_by('-time_stamp')
    return render(request, 'postelo/mesg_index.html', {'messages': messages})


def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if 'btnSend' in request.POST:
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.save()
                return redirect('message_inbox')
            else:
                return render(request, '', {'form': form})
        elif 'btnDraft' in request.POST:
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.draft = True
                message.save()
                return redirect('message_inbox')
            else:
                return render(request, '', {'form': form})

    form = MessageForm()
    return render(request, 'postelo/mesg_create.html', {'form': form})


def message_detail(request, pk):
    message = get_object_or_404(Message, id=pk)
    if message.sender != request.user:
        if not message.is_read:
            message.is_read = True
            message.save()
    return render(request, 'postelo/mesg_detail.html', {'message': message})


def message_drafts(request):
    messages = Message.objects.all().filter(sender=request.user).filter(draft=True).order_by('-time_stamp')
    return render(request, 'postelo/mesg_drafts.html', {'messages': messages})


def message_sent(request):
    messages = Message.objects.all().filter(sender=request.user).filter(draft=False).order_by('-time_stamp')
    return render(request, 'postelo/mesg_sent.html', {'messages': messages})


def message_delete(request, pk):
    message = get_object_or_404(Message, id=pk)
    message.delete()
    return redirect('message_inbox')


def message_into_trash(request, pk):
    message = get_object_or_404(Message, id=pk)
    message.is_trash = True
    message.save()
    return redirect('message_inbox')


def message_trash(request):
    messages = Message.objects.all().filter(recipient=request.user).filter(is_trash=True).order_by('-time_stamp')
    return render(request, 'postelo/mesg_trash.html', {'messages': messages})
