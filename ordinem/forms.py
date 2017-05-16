from django import forms
from .models import Ngo, Happening, Gallery, HapComments, NgoRatings


class NgoForm(forms.ModelForm):

    class Meta:
        model = Ngo
        exclude = ('moderator', 'rating', 'likes')


class HappeningForm(forms.ModelForm):

    class Meta:
        model = Happening
        exclude = ('author', 'likes')


class GalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        exclude = ('owner',)


class HapCommentsForm(forms.ModelForm):

    class Meta:
        model = HapComments
        exclude = ('author', 'comment_on')


class NgoRatingForm(forms.ModelForm):
    star_choice = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    rating = forms.ChoiceField(choices=star_choice, widget=forms.RadioSelect)

    class Meta:
        model = NgoRatings
        exclude = ('ngo', 'user')
