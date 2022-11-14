from rest_framework import viewsets, permissions, generics, mixins

from main import models, serializers


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = models.Office.objects.all()
    serializer_class = serializers.OfficeSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = models.Reservation.objects.all()
    serializer_class = serializers.ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RestViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = models.Rest.objects.all()
    serializer_class = serializers.RestSerializer


class MyUserApiView(generics.ListAPIView):
    queryset = models.MyUser.objects.all()
    serializer_class = serializers.MyUserSerializer

