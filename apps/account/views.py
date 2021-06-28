from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.account.models import User
from apps.account.serializers import CreateUserSerializer, UserActivitySerializer
from apps.utils.bot import bot_validation


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    @action(
        methods=["post"],
        detail=False,
        serializer_class=CreateUserSerializer
    )
    def register(self, request):
        if not bot_validation('User', User.objects.count()):
            return Response({'error': 'Maximum number of users'}, status=status.HTTP_400_BAD_REQUEST)
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({'data': 'You are successfully registered'}, status=status.HTTP_200_OK)
        return Response(ser.errors)


    @action(
        methods=["get"],
        detail=False,
        serializer_class=UserActivitySerializer
    )
    def last_activity(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
