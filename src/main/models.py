from django.db import models
from django.contrib.auth.models import User


class Office(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"Office {self.name}, {self.address}"


class Room(models.Model):
    number = models.CharField(max_length=15)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="office")
    capacity = models.IntegerField()

    def __str__(self):
        return f"Room #{self.number}, {self.office}"


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_reservation")
    data = models.DateField()
    reserved_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")


class Rest(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_rest")
    rest = models.IntegerField()
    date = models.DateField()