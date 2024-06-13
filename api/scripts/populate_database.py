import os
import sys
import django
import random
from django.contrib.auth import get_user_model
from django.db import transaction

project_path = os.getenv('DJANGO_PROJECT_PATH')
settings_module = os.getenv('DJANGO_SETTINGS_MODULE')

if not project_path or not settings_module:
    print("The environment variables 'DJANGO_PROJECT_PATH' and 'DJANGO_SETTINGS_MODULE' must be set.")
    sys.exit(1)

sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
django.setup()

from basketball.models import Team, Player

User = get_user_model()

TEAM_NAMES = [f'Team {i}' for i in range(1, 17)]
PLAYER_NAMES = [f'Player {i}' for i in range(1, 161)]
COACH_NAMES = [f'Coach {i}' for i in range(1, 17)]

@transaction.atomic
def populate_database():
    coaches = []
    for i, name in enumerate(COACH_NAMES):
        coach = User.objects.create_user(
            username=f'coach{i+1}',
            password='password123',
            email=f'coach{i+1}@example.com',
            first_name=name.split()[0],
            last_name=name.split()[1],
            role='coach'
        )
        coaches.append(coach)
        print(coach)
    
    for i, team_name in enumerate(TEAM_NAMES):
        team = Team.objects.create(
            name=team_name,
            coach=coaches[i],
            team_score=0,
            falts=0
        )
        
        for j in range(10):
            Player.objects.create(
                name=PLAYER_NAMES[i*10 + j],
                height=round(random.uniform(1.70, 2.10), 2),
                average_score=round(random.uniform(5, 30), 2),
                games_played=random.randint(0, 20),
                team=team
            )
            
    User.objects.create_superuser(
        username='admin',
        password='admin123',
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        role='admin'
    )
    print("Admin user created")

if __name__ == "__main__":
    populate_database()
    print("Database populated successfully!")
