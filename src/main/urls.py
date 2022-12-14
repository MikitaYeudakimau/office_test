from django.urls import path
from main import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'offices', views.OfficeViewSet, basename='offices')
router.register(r'rooms', views.RoomViewSet, basename='rooms')
router.register(r'reservation', views.ReservationViewSet, basename='reservation')
router.register(r'rest', views.RestViewSet, basename='rest')

urlpatterns = [
    path("users/", views.MyUserApiView.as_view(), name="user-list")
]

urlpatterns += router.urls
