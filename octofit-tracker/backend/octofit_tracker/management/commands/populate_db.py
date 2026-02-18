from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Workout, Activity, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):


        # Drop collections directly for Djongo/MongoDB
        from django.db import connection
        with connection.cursor() as cursor:
            for collection in ["activity", "leaderboard", "user", "workout", "team"]:
                try:
                    cursor.db_conn[collection].drop()
                except Exception:
                    pass

        # Create Teams
        marvel = Team.objects.create(name="Marvel", description="Marvel superheroes")
        dc = Team.objects.create(name="DC", description="DC superheroes")


        # Create Users (save individually for Djongo compatibility)
        user_data = [
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": marvel, "is_superhero": True},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": marvel, "is_superhero": True},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": dc, "is_superhero": True},
            {"name": "Batman", "email": "batman@dc.com", "team": dc, "is_superhero": True},
        ]
        users = []
        for data in user_data:
            user = User(**data)
            user.save()
            users.append(user)

        # Create Workouts (save individually for Djongo compatibility)
        workout_data = [
            {"name": "Web Swing", "description": "Swinging through the city", "difficulty": "Medium"},
            {"name": "Flight", "description": "Flying in the sky", "difficulty": "Hard"},
            {"name": "Combat Training", "description": "Hand-to-hand combat", "difficulty": "Hard"},
            {"name": "Gadget Training", "description": "Using superhero gadgets", "difficulty": "Medium"},
        ]
        workouts = []
        for data in workout_data:
            workout = Workout(**data)
            workout.save()
            workouts.append(workout)

        # Create Activities
        activities = [
            Activity(user=users[0], workout=workouts[0], date=timezone.now().date(), duration_minutes=30, points=100),
            Activity(user=users[1], workout=workouts[1], date=timezone.now().date(), duration_minutes=45, points=150),
            Activity(user=users[2], workout=workouts[2], date=timezone.now().date(), duration_minutes=60, points=200),
            Activity(user=users[3], workout=workouts[3], date=timezone.now().date(), duration_minutes=40, points=120),
        ]
        Activity.objects.bulk_create(activities)

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, total_points=250)
        Leaderboard.objects.create(team=dc, total_points=320)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
