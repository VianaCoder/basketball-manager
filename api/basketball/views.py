from rest_framework import viewsets
from basketball import serializers, models
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrCoachOfPlayerTeam, IsAdminUser, BasePermission
from rest_framework.views import APIView
from .models import Player, Team, User
import numpy as np

class IsAdminOrCoachPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or (request.user.is_authenticated and request.user.role == 'coach'):
            return True
        return False

class PlayersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PlayerSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return models.Player.objects.all()
        elif user.role == 'coach':
            if hasattr(user, 'coached_team'):
                return models.Player.objects.filter(team=user.coached_team)
            else:
                return models.Player.objects.none() 
        else:
            return models.Player.objects.none()

    @action(detail=False, methods=['get'], url_path='high-scorers', url_name='high_scorers')
    def high_scorers(self, request, *args, **kwargs):
        user = request.user
        
        if user.role != 'coach':
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        
        if not hasattr(user, 'coached_team'):
            return Response({'detail': 'You do not have a team assigned.'}, status=status.HTTP_400_BAD_REQUEST)
        
        team = user.coached_team
        players = team.player_set.all()
        
        if not players.exists():
            return Response({'detail': 'No players in your team.'}, status=status.HTTP_400_BAD_REQUEST)
        
        average_scores = players.values_list('average_score', flat=True)
        percentile_90 = np.percentile(average_scores, 90)
        
        high_scorers = players.filter(average_score__gte=percentile_90)
        serializer = self.get_serializer(high_scorers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeamsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()

class GamesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GameSerializer
    queryset = models.Game.objects.all()

class UserRegistrationViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
class PlayerDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrCoachOfPlayerTeam]

    def get(self, request, player_id):
        try:
            player = Player.objects.get(pk=player_id)
            
            self.check_object_permissions(request, player)
            
            serializer = serializers.PlayerSerializer(player)
            return Response(serializer.data)
        except Player.DoesNotExist:
            return Response({'message': 'Player not found'}, status=404)

