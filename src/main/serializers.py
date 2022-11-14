from main import models
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Office
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    office = serializers.SlugRelatedField(queryset=models.Office.objects.all(), slug_field="name")

    class Meta:
        model = models.Room
        fields = ['id', 'number', 'capacity', 'office']

    def validate(self, data):
        if data['capacity'] < 1:
            raise serializers.ValidationError("Capacity cannot be less than 1")
        return data


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ['id', 'room', 'date', 'user', 'reserved_at']
        validators = [
            UniqueTogetherValidator(
                queryset=models.Reservation.objects.all(),
                fields=['room', 'date', 'user']
            )
        ]

    def create(self, validated_data):
        room = validated_data["room"]
        date = validated_data["date"]
        user = validated_data["user"]
        capacity = models.Room.objects.get(pk=room.pk).capacity
        obj, created = models.Rest.objects.get_or_create(
            room=room,
            date=date,
            defaults={'rest': capacity}
        )
        if obj.rest == 0:
            raise serializers.ValidationError("There are no more spare places. "
                                              "Please choose another date or room")
        else:
            obj.rest -= 1
            obj.save()
            obj.user_rest.add(user)
        return models.Reservation.objects.create(**validated_data)


class RestSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField()
    user_rest = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Rest
        fields = '__all__'


class MyUserSerializer(serializers.ModelSerializer):
    reservation_user = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.MyUser
        fields = ['username', 'email', 'is_staff', 'reservation_user']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['reservation_amount'] = instance.reservation_user.count()

        return ret
