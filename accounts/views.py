from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from accounts.forms import SignUpForm, UserLoginForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from ordinem.models import Happening
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied


def home(request):
    return render(request, 'accounts/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def profile_view(request):
    current_user = request.user
    return render(request, 'accounts/profile.html', {'current_user': current_user})


def profile_detail(request, pk):
    current_user = get_object_or_404(User, id=pk)
    return render(request, 'accounts/profile.html', {'current_user': current_user})


def profile_edit(request, pk):
    # get User object from db
    user = User.objects.get(pk=pk)

    # prepopulate the form with user data
    user_form = UserForm(request.POST or None, instance=user)

    # Appending the user form with user profile form
    ProfileInlineFormset = inlineformset_factory(User, UserProfile, form=UserProfileForm, can_delete=False)
    formset = ProfileInlineFormset(request.POST or None, request.FILES or None, instance=user)

    if request.user.is_authenticated():
        if request.method == 'POST':
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return redirect('profile')
                else:
                    return render(request, 'accounts/profileedit.html', {
                        'noodle': pk,
                        'form': user_form,
                        'formset': formset,
                    })

            else:
                return render(request, 'accounts/profileedit.html', {
                    'noodle': pk,
                    'form': user_form,
                    'formset': formset,
                })
        else:
            return render(request, 'accounts/profileedit.html', {
                'noodle': pk,
                'form': user_form,
                'formset': formset,
            })
    else:
        raise PermissionDenied


@login_required()
def feeds_view(request):
    user = request.user
    user_profile = UserProfile.objects.get(id=user.pk)
    ngos = user_profile.follows.all()
    happenings = Happening.objects.filter(author__in=ngos)
    return render(request, 'accounts/user_feeds.html', {'ngos': ngos, 'happenings': happenings})
