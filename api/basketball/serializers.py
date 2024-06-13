from rest_framework import serializers
from .models import *

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'height', 'average_score', 'games_played', 'team']
    
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'coach', 'team_score', 'falts']

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'team1', 'team2', 'team1_score', 'team2_score', 'winning_team', 'date']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user