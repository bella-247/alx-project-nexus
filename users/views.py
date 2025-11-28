from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class LoginView(TokenObtainPairView):
    """Override token obtain to return user info together with access token.

    Response shape: {"user": <user>, "token": "<access>"}
    """

    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tokens = serializer.validated_data
        user = getattr(serializer, 'user', None)
        user_data = None
        if user is not None:
            user_data = UserSerializer(user).data

        # Preserve standard simplejwt keys for compatibility and include user
        response_payload = {}
        if 'access' in tokens:
            response_payload['access'] = tokens.get('access')
        if 'refresh' in tokens:
            response_payload['refresh'] = tokens.get('refresh')
        response_payload['user'] = user_data

        return Response(response_payload, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
