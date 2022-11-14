from django.contrib.auth.models import AbstractUser
from django.db import models


class Office(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"Office {self.name}, {self.address}"


class Room(models.Model):
    number = models.CharField(max_length=15)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="room_office")
    capacity = models.IntegerField()

    def __str__(self):
        return f"Room #{self.number}, {self.office}"

    class Meta:
        unique_together = ('number', 'office')


class Rest(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="rest_room")
    rest = models.IntegerField()
    date = models.DateField()


class MyUser(AbstractUser):
    rest = models.ManyToManyField(Rest, related_name="user_rest")


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservation_room")
    date = models.DateField()
    reserved_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="reservation_user")

    def __str__(self):
        return f"{self.user} reserve {self.room} at {self.date}"
