from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'
    
class IsAdminOrCoachOfPlayerTeam(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        
        if hasattr(obj, 'team') and hasattr(request.user, 'coached_team'):
            return obj.team.coach == request.user.coached_team
        
        return False