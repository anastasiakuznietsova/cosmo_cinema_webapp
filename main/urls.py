from django.urls import path
from main import views

app_name = 'main'
urlpatterns = [
    path('api/showtime/',views.ShowtimeList.as_view(), name='showtime'),
    path('api/showtime/create/', views.ShowtimeCreate.as_view(), name='create-showtime'),
    path('api/showtime/<int:pk>', views.ShowtimeDelete.as_view(), name='delete-show'),

    path('api/users/', views.UserDetail.as_view(), name ='user-info'),
    path('api/users/update/', views.UserUpdate.as_view(), name ='user-info-update'),
    path('api/users/delete/', views.UserDelete.as_view(), name ='user-delete'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),

    path('api/movies/', views.MovieList.as_view(), name='movies'),
    path('api/movies/<int:pk>/', views.MovieDetails.as_view(), name='movie-details'),
    path('api/movies/create/', views.MovieCreate.as_view(), name='create-movie'),
    path('api/movies/<int:pk>/update/',views.MovieUpdate.as_view(), name='update-movie'),
    path('api/movies/<int:pk>/delete/',views.MovieDelete.as_view(), name='delete-movie'),

    path('api/tickets/', views.TicketBooking.as_view(), name='book-a-ticket'),
    path('api/tickets/<int:pk>/', views.TicketCanceling.as_view(), name='cancel-ticket'),
]