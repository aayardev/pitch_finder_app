from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from django.contrib.auth import get_user_model
from core.models import Pitch, Reservation
from .serializers import (
    PitchSerializer,
    ReservationSerializer,
    UserSerializer,
    AuthTokenSerializer,
)
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


User = get_user_model()


class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


signup_view = SignupView.as_view()


class LoginView(GenericAPIView):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


login_view = LoginView.as_view()


class PitchListAPIView(ListAPIView):
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer


pitch_list_api_view = PitchListAPIView.as_view()


class ReservationCreateAPIView(CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


reservation_create_api_view = ReservationCreateAPIView.as_view()
