from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile
from django import forms
import datetime

#user = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(required=False, help_text='Optional.')
    last_name = forms.CharField(required=False, help_text='Optional.')
    email = forms.EmailField(help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):

    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1960, datetime.datetime.now().year)))

    class Meta:
        model = UserProfile
        fields = ('birth_date', 'gender', 'photo', 'city', 'country', 'bio')
        exclude = ('follow',)


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-lg",
                                                                      'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control input-lg",
                                                                 'placeholder': 'password'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Wrong Password")
            if not user.is_active:
                raise forms.ValidationError("This User is no Longer Active..")
            return super(UserLoginForm, self).clean(*args, **kwargs)