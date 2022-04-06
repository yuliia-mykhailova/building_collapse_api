from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from .models import *


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'email', 'password', 'access', 'refresh']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'access', 'refresh']

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        token = user.token

        return {
            'email': user.email,
            'access': token.access_token,
            'refresh': token
        }


class LogoutSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['refresh']

    def validate(self, data):
        self.token = data.get('refresh', None)
        return data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('Bad token')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'phone', 'email']


class CreateConstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Construction
        fields = '__all__'


class FoundationSerializer(serializers.ModelSerializer):
    foundation_type = serializers.CharField(source='get_foundation_type_display')
    foundation_material = serializers.CharField(source='get_foundation_material_display')

    class Meta:
        model = Foundation
        fields = '__all__'


class RoofSerializer(serializers.ModelSerializer):
    roof_type = serializers.CharField(source='get_roof_type_display')
    roof_material = serializers.CharField(source='get_roof_material_display')

    class Meta:
        model = Roof
        fields = '__all__'


class CreateFoundationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foundation
        fields = '__all__'


class CreateRoofSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roof
        fields = '__all__'


class WallsSerializer(serializers.ModelSerializer):
    walls_material = serializers.CharField(source='get_walls_material_display')

    class Meta:
        model = Walls
        fields = '__all__'


class CreateWallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Walls
        fields = '__all__'


class FloorSerializer(serializers.ModelSerializer):
    floor_type = serializers.CharField(source='get_floor_type_display')

    class Meta:
        model = Floor
        fields = '__all__'


class CreateFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'


class ConstructionSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer()
    roof = RoofSerializer()
    walls = WallsSerializer()
    floor = FloorSerializer()
    foundation = FoundationSerializer()
    construction_type = serializers.CharField(source='get_construction_type_display')

    class Meta:
        model = Construction
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    construction = ConstructionSerializer

    class Meta:
        model = Measurement
        fields = '__all__'


class CreateMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'


class EvaluationSerializer(serializers.ModelSerializer):
    measurement = MeasurementSerializer

    class Meta:
        model = Evaluation
        fields = '__all__'


class CreateEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'


class PredictionSerializer(serializers.ModelSerializer):
    construction = ConstructionSerializer

    class Meta:
        model = Prediction
        fields = '__all__'


class CreatePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'
