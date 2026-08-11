from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ClinorynTokenObtainPairSerializer, UserMeSerializer


class ClinorynTokenObtainPairView(TokenObtainPairView):
    serializer_class = ClinorynTokenObtainPairSerializer


class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=UserMeSerializer)
    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)
