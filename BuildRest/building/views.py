from django_filters import rest_framework as filters
from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .evaluate import evaluate
from .serializers import *
from .predict import *


class RegisterAPIView(APIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomUserViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser | IsAuthenticated, ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(email=self.request.user)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get(self, request):
        user = CustomUser.objects.get(email=self.request.user)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConstructionFilter(filters.FilterSet):
    CONSTRUCTION_TYPES = [
        ('1', 'Residential'),
        ('2', 'Historical'),
        ('3', 'Another'),
    ]

    ROOF_TYPES = [
        ('1', 'Gable'),
        ('2', 'Hip'),
        ('3', 'Dutch'),
        ('4', 'Mansard'),
        ('5', 'Flat'),
        ('6', 'Shed'),
        ('7', 'Butterfly'),
        ('8', 'Gambrel'),
        ('9', 'Dormer'),
        ('10', 'M Shaped'),
        ('11', 'Combined'),
    ]

    MATERIALS = [
        ('1', 'Wood'),
        ('2', 'Brick'),
        ('3', 'Vinyl'),
        ('4', 'Metal'),
        ('5', 'Stone'),
        ('6', 'Concrete'),
        ('7', 'Plastic'),
        ('8', 'Another'),
    ]

    FOUNDATION_TYPES = [
        ('1', 'Strip'),
        ('2', 'Columnar'),
        ('3', 'Pile'),
        ('4', 'Panel-wall'),
        ('5', 'Screw'),
        ('6', 'Another'),
    ]

    ORDER_CHOICES = [
        ('name', 'Sort Alphabetically (A to Z)'),
        ('-name', 'Sort Alphabetically (Z to A)'),
        ('build_date', 'Sort by build date (ascending)'),
        ('-build_date', 'Sort by build date (descending)'),
    ]

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    address = filters.CharFilter(field_name='address', lookup_expr='icontains')

    construction_type = filters.MultipleChoiceFilter(field_name='construction_type', choices=CONSTRUCTION_TYPES)

    min_height = filters.NumberFilter(field_name="height", lookup_expr='gte')
    max_height = filters.NumberFilter(field_name="height", lookup_expr='lte')

    min_floor = filters.NumberFilter(field_name="floor_number", lookup_expr='gte')
    max_floor = filters.NumberFilter(field_name="floor_number", lookup_expr='lte')

    min_build_date = filters.DateFilter(field_name="build_date", lookup_expr='gte')
    max_build_date = filters.DateFilter(field_name="build_date", lookup_expr='lte')

    min_total_area = filters.NumberFilter(field_name="total_area", lookup_expr='gte')
    max_total_area = filters.NumberFilter(field_name="total_area", lookup_expr='lte')

    roof_type = filters.MultipleChoiceFilter(field_name='roof__roof_type', choices=ROOF_TYPES)
    roof_material = filters.MultipleChoiceFilter(field_name='roof__roof_material', choices=MATERIALS)

    walls_material = filters.MultipleChoiceFilter(field_name='walls__walls_material', choices=MATERIALS)
    min_walls_thickness = filters.NumberFilter(field_name='walls__thickness', lookup_expr='gte')
    max_walls_thickness = filters.NumberFilter(field_name='walls__thickness', lookup_expr='lte')

    floor_material = filters.MultipleChoiceFilter(field_name='floor__floor_type', choices=MATERIALS)

    foundation_type = filters.MultipleChoiceFilter(field_name='foundation__foundation_type', choices=FOUNDATION_TYPES)
    foundation_material = filters.MultipleChoiceFilter(field_name='foundation__foundation_material', choices=MATERIALS)
    min_foundation_area = filters.NumberFilter(field_name='foundation__area', lookup_expr='gte')
    max_foundation_area = filters.NumberFilter(field_name='foundation__area', lookup_expr='lte')

    order_by = filters.OrderingFilter(choices=ORDER_CHOICES)

    class Meta:
        model = Construction
        fields = ['name',
                  'construction_type',
                  'address',
                  'min_height',
                  'max_height',
                  'min_floor',
                  'max_floor',
                  'min_build_date',
                  'max_build_date',
                  'min_total_area',
                  'max_total_area',
                  'roof_type',
                  'roof_material',
                  'walls_material',
                  'min_walls_thickness',
                  'max_walls_thickness',
                  'floor_material',
                  'foundation_type',
                  'foundation_material',
                  'min_foundation_area',
                  'max_foundation_area',
                  ]


class ConstructionViewSet(ModelViewSet):
    serializer_class = CreateConstructionSerializer
    filter_class = ConstructionFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.serializer_class = ConstructionSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [IsAdminUser | IsAuthenticated, ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = CustomUser.objects.get(email=self.request.user)
        result_set = Construction.objects.all()
        if not user.is_superuser:
            result_set = Construction.objects.filter(owner_id=user.id)
        if not(self.action == 'update' or self.action == 'partial_update'):
            result_set = result_set.select_related('roof', 'walls', 'floor', 'foundation')
        return result_set


class FoundationViewSet(ModelViewSet):
    serializer_class = CreateFoundationSerializer
    permission_classes = [IsAdminUser | IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.serializer_class = FoundationSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Foundation.objects.all()
        return Foundation.objects.filter(construction__owner=self.request.user)


class RoofViewSet(ModelViewSet):
    serializer_class = CreateRoofSerializer
    permission_classes = [IsAdminUser | IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.serializer_class = RoofSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Roof.objects.all()
        return Roof.objects.filter(construction__owner=self.request.user)


class WallsViewSet(ModelViewSet):
    serializer_class = CreateWallsSerializer
    permission_classes = [IsAdminUser | IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.serializer_class = WallsSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Walls.objects.all()
        return Walls.objects.filter(construction__owner=self.request.user)


class FloorViewSet(ModelViewSet):
    serializer_class = CreateFloorSerializer
    permission_classes = [IsAdminUser | IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.serializer_class = FloorSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Floor.objects.all()
        return Floor.objects.filter(construction__owner=self.request.user)


class MeasurementFilter(filters.FilterSet):
    min_measurement_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    max_measurement_date = filters.DateFilter(field_name="date", lookup_expr='lte')

    construction = filters.CharFilter(field_name="construction__name", lookup_expr='icontains')

    class Meta:
        model = Measurement
        fields = ['min_measurement_date', 'max_measurement_date', 'construction', ]


class MeasurementViewSet(ModelViewSet):
    serializer_class = CreateMeasurementSerializer
    permission_classes = [IsAdminUser | IsAuthenticated, ]
    filter_class = MeasurementFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.serializer_class = MeasurementSerializer
        return self.serializer_class

    def get_queryset(self):
        user = CustomUser.objects.get(email=self.request.user)
        if user.is_superuser:
            return Measurement.objects.all()
        return Measurement.objects.filter(construction__owner=self.request.user)


class EvaluationFilter(filters.FilterSet):
    min_evaluation_date = filters.DateFilter(field_name="measurement__date", lookup_expr='gte')
    max_evaluation_date = filters.DateFilter(field_name="measurement__date", lookup_expr='lte')

    construction = filters.CharFilter(field_name="measurement__construction__name", lookup_expr='icontains')

    class Meta:
        model = Evaluation
        fields = ['min_evaluation_date', 'max_evaluation_date', 'construction', ]


class EvaluationViewSet(ModelViewSet):
    permission_classes = [IsAdminUser | IsAuthenticated, ]
    serializer_class = EvaluationSerializer
    filter_class = EvaluationFilter

    def create(self, request, *args, **kwargs):
        measurement_id = request.data.get('measurement')
        user = CustomUser.objects.get(email=self.request.user)
        queryset = Construction.objects.filter(owner_id=user.id).values_list('id', flat=True)
        measurement = Measurement.objects.get(id=measurement_id)
        if measurement.construction_id in queryset or user.is_superuser:
            build_date = Construction.objects.get(id=measurement.construction_id)
            roof = Roof.objects.get(construction_id=measurement.construction_id)
            walls = Walls.objects.get(construction_id=measurement.construction_id)
            floor = Floor.objects.get(construction_id=measurement.construction_id)
            foundation = Foundation.objects.get(construction_id=measurement.construction_id)
            result = (evaluate(measurement_id, build_date.build_date,
                               [roof.roof_material, walls.walls_material, floor.floor_type,
                                foundation.foundation_material],
                               measurement.humidity, measurement.acoustic_analysis, measurement.vibration))
            serializer = CreateEvaluationSerializer(data=result)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise PermissionDenied

    def get_queryset(self):
        user = CustomUser.objects.get(email=self.request.user)
        if user.is_superuser:
            return Evaluation.objects.all()
        else:
            return Evaluation.objects.filter(measurement__construction__owner=self.request.user)


class PredictionFilter(filters.FilterSet):
    min_prediction_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    max_prediction_date = filters.DateFilter(field_name="date", lookup_expr='lte')

    construction = filters.CharFilter(field_name="construction__name", lookup_expr='icontains')

    class Meta:
        model = Prediction
        fields = ['min_prediction_date', 'max_prediction_date', 'construction', ]


class PredictionViewSet(ModelViewSet):
    serializer_class = PredictionSerializer
    queryset = Prediction.objects.all()
    permission_classes = [IsAdminUser | IsAuthenticated, ]
    filter_class = PredictionFilter

    def create(self, request, *args, **kwargs):
        construction_id = request.data.get('construction')
        user = CustomUser.objects.get(email=self.request.user)
        if user.is_superuser:
            queryset = Construction.objects.all()
        else:
            queryset = Construction.objects.filter(owner_id=user.id).values_list('id', flat=True)
        if construction_id in queryset or user.is_superuser:
            evaluation_id = Measurement.objects.filter(construction_id=construction_id).order_by('id').last()
            evaluation_data = Evaluation.objects.get(measurement_id=evaluation_id)
            build_date = Construction.objects.get(id=construction_id)
            result = prediction(construction_id, evaluation_data.final_coefficient, build_date.build_date)
            serializer = CreatePredictionSerializer(data=result)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise PermissionDenied

    def get_queryset(self):
        user = CustomUser.objects.get(email=self.request.user)
        if user.is_superuser:
            return Prediction.objects.all()
        else:
            return Prediction.objects.filter(construction__owner=self.request.user)
