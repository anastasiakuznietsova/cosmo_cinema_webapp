from urllib.request import Request

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from .serializers import MovieSerializer,UserSerializer, TicketSerializer, ShowtimeSerializer
from rest_framework import status, generics, authentication, permissions

from .models import Ticket, Showtime, Movie
from .forms import RegistrationForm


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('main:showtime')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main:showtime')
            else:
                form.add_error(None, "Invalid username or password")

    return render(request, 'main/login.html', {'form': form})
def registerPage(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('main:showtime')
    else:
        form=RegistrationForm()
    return render(request, 'main/register.html', {'form': form})
@permission_classes([IsAuthenticated])
def logoutPage(request):
    logout(request)
    return redirect('main:showtime')


class UserDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/viewer_info.html"

    def get_tickets(self,user):
        return Ticket.objects.filter(user=user)
    def get(self,request):
        if request.user.is_authenticated:
            user=get_object_or_404(User, username=request.user.username)
            tickets = self.get_tickets(user)
            serializer = UserSerializer(user)
            return Response({"serializer":serializer,
                             "user":user,
                             "tickets":tickets})
        else:
            return redirect('main:login')
class UserUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name ='main/update.html'

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user)
        return Response({"serializer": serializer, "user": user})
    def post(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user,data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "user": user})
        serializer.save()
        return redirect('main:user-info')
class UserDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main/delete.html'
    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user)
        return Response({"serializer": serializer, "user": user})
    def post(self, request):
        user = get_object_or_404(User, username=request.user.username)
        logout(request)
        user.delete()
        return reverse_lazy('main:showtime')

class TicketBooking(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/create.html"
    def get(self, request):
        if request.user.is_authenticated:
            serializer = TicketSerializer()
            return Response({"serializer": serializer})
        else:
            return redirect('main:login')

    def post(self, request):
        if request.user.is_authenticated:
            serializer = TicketSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return redirect('main:showtime')
            return redirect('main:showtime')
        else:
            return redirect('main:login')
class TicketCanceling(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main/delete.html'
    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        serializer = TicketSerializer(ticket)
        return Response({"serializer": serializer, "ticket": ticket})

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        ticket.delete()
        return redirect('main:user-info')

class ShowtimeUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/update.html"

    def get(self, request, pk):
        show = get_object_or_404(Showtime, pk=pk)
        serializer = MovieSerializer(show)
        return Response({"serializer": serializer, "show": show})
    def put(self, request, pk):
        if request.user.is_superuser:
            show = get_object_or_404(Movie, pk=pk)
            serializer = MovieSerializer(show, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"serializer": serializer, "show": show})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ShowtimeList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name="main/showtime.html"

    def get (self,request, format=None):
        queryset=Showtime.objects.all()
        return Response({"showtime":queryset})
class ShowtimeCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name="main/create.html"

    def get(self, request, format=None):
        serializer = ShowtimeSerializer()
        return Response({"serializer": serializer})
    def post(self,request, format=None):
        if request.user.is_superuser:
            serializer = ShowtimeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return redirect('main:showtime')
            return Response({"serializer": serializer}, template_name="main/create.html")
class ShowtimeDelete(APIView):
    permission_classes = [IsAdminUser]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main/delete.html'
    def get(self, request, pk):
        show = get_object_or_404(Showtime, pk=pk)
        serializer = ShowtimeSerializer(show)
        return Response(serializer.data)

    def post(self, request, pk):
        show = get_object_or_404(Showtime, pk=pk)
        if request.user.is_superuser:
            show.delete()
            return redirect('main:showtime')
        return Response(status=status.HTTP_403_FORBIDDEN)


class MovieList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main/movies.html'

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response({'movies':serializer.data})
class MovieDetails(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/movie_details.html"

    def get(self,request, pk):
        movie=get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(movie)
        return Response({"serializer":serializer,
                         "movie":movie})
class MovieCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/create.html"
    def get(self, request, format=None):
        serializer = MovieSerializer()
        return Response({"serializer": serializer})
    def post(self, request):
        if request.user.is_superuser:
            serializer = MovieSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return redirect('main:showtime')
            return redirect('main:showtime')
class MovieUpdate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name ='main/update.html'

    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(movie)
        return Response({"serializer": serializer, "movie": movie})

    def post(self, request, pk):
        if request.user.is_superuser:
            movie = get_object_or_404(Movie, pk=pk)
            serializer = MovieSerializer(movie, data=request.data)
            if not serializer.is_valid():
                return Response({"serializer": serializer, "movie": movie})
            serializer.save()
            return redirect('main:showtime')
class MovieDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main/delete.html'
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(movie)
        return Response({"serializer": serializer, "movie": movie})

    def post(self, request, pk):
        if request.user.is_superuser:
            movie = get_object_or_404(Movie, pk=pk)
            movie.delete()
            return reverse_lazy('main:showtime')
        return Response(status=status.HTTP_403_FORBIDDEN)