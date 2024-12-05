from .models import Ticket, Showtime,Movie
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['showtime','seat_num']

class ShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Showtime
        fields=['id','show_date',
                'price', 'movie', 'room', 'startsAt', 'endsAt']


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['id','title', 'premiere', 'moviegenre','agerestrictions',
                  'animationformat','mov_length','premiere','mvdescription']