from bicycles.models import Bicycle, BicycleUser
from rest_framework import serializers
from users.models import UserBill


class BicycleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ("name", "cost_per_minute")


class BicycleViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ("id", "name", "cost_per_minute")


class BicycleRentSerializer(serializers.Serializer):
    rent = serializers.BooleanField()
    bicycle = serializers.PrimaryKeyRelatedField(queryset=Bicycle.objects.all())

    def validate(self, attrs):
        user = self.context.get("user")
        if attrs["rent"]:
            bicycle_user = BicycleUser.objects.filter(user=user).first()
            if bicycle_user:
                raise serializers.ValidationError("Вы уже арендовали велосипед")
            bicycle_user = BicycleUser.objects.filter(bicycle=attrs["bicycle"]).first()
            if bicycle_user:
                raise serializers.ValidationError("Велосипед уже арендован")
        else:
            bicycle_user = BicycleUser.objects.filter(user=user).first()
            if not bicycle_user:
                raise serializers.ValidationError("Вы не арендовали велосипед")
            bicycle_user = BicycleUser.objects.filter(user=user, bicycle=attrs["bicycle"]).first()
            if not bicycle_user:
                raise serializers.ValidationError("Вы арендовали другой велосипед")
        return attrs


class RentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBill
        fields = ("id", "bill", "created_at")
