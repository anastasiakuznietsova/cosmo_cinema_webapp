from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Movie,Showtime,Ticket

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
        ]

class ShowtimeForm(forms.ModelForm):
    class Meta:
        model=Showtime
        fields = '__all__'

class TicketForm(forms.ModelForm):
    class Meta:
        model=Ticket
        fields = '__all__'


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie

        fields = '__all__'