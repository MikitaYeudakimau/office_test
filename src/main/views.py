import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics, mixins
from rest_framework.filters import SearchFilter, OrderingFilter

from main import models, serializers


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = models.Office.objects.all()
    serializer_class = serializers.OfficeSerializer
    permission_classes = (permissions.IsAdminUser,)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = (permissions.IsAdminUser,)


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReservationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['room', 'date', 'user']
    search_fields = ['user__username']
    ordering_fields = ['date']

    def get_queryset(self):
        if self.request.user.is_staff == False:
            return models.Reservation.objects.filter(user=self.request.user)
        else:
            return models.Reservation.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RestViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = models.Rest.objects.all()
    serializer_class = serializers.RestSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['room', 'date']
    search_fields = ['room']
    ordering_fields = ['date', 'rest']

    def get_queryset(self):
        if self.request.user.is_staff == False:
            return models.Rest.objects.filter(date__gte=datetime.date.today())
        else:
            return models.Rest.objects.all()


class MyUserApiView(generics.ListAPIView):
    queryset = models.MyUser.objects.all()
    serializer_class = serializers.MyUserSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username',]
    ordering_fields = ['username',]
