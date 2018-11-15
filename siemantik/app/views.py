from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from siemantik.app.serializers import UserSerializer

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer