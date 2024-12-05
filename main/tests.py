from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Movie, Showtime, MovieGenre, AgeRestrictions, AnimationFormat, Room


class TestBooking(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='kebab',password='15555322new',
                            first_name='kebab', last_name='kebabovich',
                            email='kebab@gmail.com')
        genre=MovieGenre.objects.create(id=1,genre_name='aaaa')
        restriction=AgeRestrictions.objects.create(id=1, restriction='test')
        format=AnimationFormat.objects.create(id=1, anima_format='2D')
        movie=Movie.objects.create(id=1, title='aaaaaa',mov_length=180,
                             premiere='2024-12-01',mvdescription='aaaaaa',
                             moviegenre=genre, agerestrictions=restriction, animationformat=format)
        room=Room.objects.create(id=1, room_number=1,seats_available=50)
        Showtime.objects.create(id=1,
                                movie=movie,
                                room=room,
                                price=15,
                                show_date='2024-12-01',
                                startsAt='18:00:00',
                                endsAt='20:00:00',)

    def test_booking_correct(self):
        showtime_existence = Showtime.objects.filter(id=1).exists()
        self.assertTrue(showtime_existence)
    def test_booking_incorrect(self):
        showtime_existence = Showtime.objects.filter(id=250).exists()
        self.assertFalse(showtime_existence)


class TestMovieCreate(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='seiiilyw',password='030615kuza')
        genre = MovieGenre.objects.create(id=1, genre_name='aaaa')
        restriction = AgeRestrictions.objects.create(id=1, restriction='test')
        format = AnimationFormat.objects.create(id=1, anima_format='2D')
        cls.movie=Movie.objects.create(id=1, title='aaaaaa',mov_length=180,
                             premiere='2024-12-01',mvdescription='aaaaaa',
                             moviegenre=genre, agerestrictions=restriction, animationformat=format)
    def test_movie_createcorrect(self):
        self.assertIsInstance(self.movie, Movie)
        self.assertEqual(self.movie.title, 'aaaaaa')
    def test_movie_create_title_incorrect(self):
        self.assertNotEqual(self.movie.title, '123')


class TestIntegration(APITestCase):
    def setUp(self):
        self.user=User.objects.create(username='seiiilyw',password='030615kuza')
        self.client.force_authenticate(user=self.user)
    def test_post_reques(self):
        data = {'title': 'aaaaaa',
        'mov_length': 180,
        'premiere': '2024-12-01',
        'mvdescription': 'aaaaaa',
        'moviegenre': 1,
        'agerestrictions': 1,
        'animationformat': 1,}
        response=self.client.post('api/movies/create/',data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)