from django.test import TestCase
from .models import User, Team, Workout, Activity, Leaderboard
from django.utils import timezone

class ModelTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Marvel", description="Marvel superheroes")
        self.user = User.objects.create(name="Spider-Man", email="spiderman@marvel.com", team=self.team, is_superhero=True)
        self.workout = Workout.objects.create(name="Web Swing", description="Swinging through the city", difficulty="Medium")
        self.activity = Activity.objects.create(user=self.user, workout=self.workout, date=timezone.now().date(), duration_minutes=30, points=100)
        self.leaderboard = Leaderboard.objects.create(team=self.team, total_points=100)

    def test_user_creation(self):
        self.assertEqual(self.user.name, "Spider-Man")
        self.assertEqual(self.user.team.name, "Marvel")

    def test_activity_points(self):
        self.assertEqual(self.activity.points, 100)

    def test_leaderboard_points(self):
        self.assertEqual(self.leaderboard.total_points, 100)
