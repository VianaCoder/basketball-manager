from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from uuid import uuid4

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('coach', 'Coach'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    coach = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, related_name='coached_team')
    team_score = models.IntegerField()
    falts = models.IntegerField(default=0)

    def sum_score(self, new_score: int):
        self.team_score += new_score

class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    height = models.FloatField()
    average_score = models.FloatField()
    games_played = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    team1_score = models.IntegerField()
    team2_score = models.IntegerField()
    winning_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_games')
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.team1_score > self.team2_score:
            self.winning_team = self.team1
        elif self.team1_score < self.team2_score:
            self.winning_team = self.team2
        else:
            self.winning_team = None  
        super().save(*args, **kwargs)