from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(unique=True, max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        refresh = RefreshToken.for_user(self)
        return refresh


class Construction(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CONSTRUCTION_TYPES = [
        ('1', 'Residential'),
        ('2', 'Historical'),
        ('3', 'Another'),
    ]
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=100, blank=False)
    construction_type = models.CharField(choices=CONSTRUCTION_TYPES, default='3', max_length=1)
    height = models.DecimalField(max_digits=100, decimal_places=2)
    floor_number = models.IntegerField(default=1)
    build_date = models.DateField()
    total_area = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}".format(self.name,
                                                   self.address,
                                                   self.get_construction_type_display(),
                                                   self.height,
                                                   self.floor_number,
                                                   self.build_date,
                                                   self.total_area)


class Foundation(models.Model):
    FOUNDATION_TYPES = [
        ('1', 'Strip'),
        ('2', 'Columnar'),
        ('3', 'Pile'),
        ('4', 'Panel-wall'),
        ('5', 'Screw'),
        ('6', 'Another'),
    ]
    FOUNDATION_MATERIALS = [
        ('1', 'Wood'),
        ('2', 'Brick'),
        ('3', 'Vinyl'),
        ('4', 'Metal'),
        ('5', 'Stone'),
        ('6', 'Concrete'),
        ('7', 'Plastic'),
        ('8', 'Another'),
    ]
    construction = models.OneToOneField(Construction, on_delete=models.CASCADE, primary_key=True)
    area = models.DecimalField(max_digits=100, decimal_places=2, default=0, blank=True)
    foundation_type = models.CharField(choices=FOUNDATION_TYPES, default='6', max_length=20)
    foundation_material = models.CharField(choices=FOUNDATION_MATERIALS, default='8', max_length=20)

    def __str__(self):
        return "{}, {}, {}".format(self.area,
                                   self.get_foundation_type_display(),
                                   self.get_foundation_material_display())


class Roof(models.Model):
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

    ROOF_MATERIALS = [
        ('1', 'Wood'),
        ('2', 'Brick'),
        ('3', 'Vinyl'),
        ('4', 'Metal'),
        ('5', 'Stone'),
        ('6', 'Concrete'),
        ('7', 'Plastic'),
        ('8', 'Another'),
    ]
    construction = models.OneToOneField(Construction, on_delete=models.CASCADE, primary_key=True)
    roof_type = models.CharField(choices=ROOF_TYPES, default='11', max_length=20)
    roof_material = models.CharField(choices=ROOF_MATERIALS, default='8', max_length=20)

    def __str__(self):
        return "{}, {}".format(self.get_roof_type_display(),
                               self.get_roof_material_display())


class Walls(models.Model):
    WALLS_MATERIALS = [
        ('1', 'Wood'),
        ('2', 'Brick'),
        ('3', 'Vinyl'),
        ('4', 'Metal'),
        ('5', 'Stone'),
        ('6', 'Concrete'),
        ('7', 'Plastic'),
        ('8', 'Another'),
    ]
    construction = models.OneToOneField(Construction, on_delete=models.CASCADE, primary_key=True)
    walls_material = models.CharField(choices=WALLS_MATERIALS, default='8', max_length=1)
    thickness = models.DecimalField(max_digits=100, decimal_places=2, blank=True)

    def __str__(self):
        return "{}, {}".format(self.get_walls_material_display(),
                               self.thickness)


class Floor(models.Model):
    FLOOR_TYPES = [
        ('1', 'Wood'),
        ('2', 'Brick'),
        ('3', 'Vinyl'),
        ('4', 'Metal'),
        ('5', 'Stone'),
        ('6', 'Concrete'),
        ('7', 'Plastic'),
        ('8', 'Another'),
    ]
    construction = models.OneToOneField(Construction, on_delete=models.CASCADE, primary_key=True)
    floor_type = models.CharField(choices=FLOOR_TYPES, default='8', max_length=1)

    def __str__(self):
        return "{}".format(self.get_floor_type_display())


class Measurement(models.Model):
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=100, decimal_places=3, blank=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    acoustic_analysis = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)
    vibration = models.DecimalField(max_digits=100, decimal_places=3, blank=True)

    def __str__(self):
        return "{}, {}, {}, {}".format(self.date,
                                       self.temperature,
                                       self.humidity,
                                       self.vibration)


class Evaluation(models.Model):
    measurement = models.OneToOneField(Measurement, on_delete=models.CASCADE, primary_key=True)
    foundation_mark = models.DecimalField(max_digits=100, decimal_places=2, blank=True)
    floor_mark = models.DecimalField(max_digits=6, decimal_places=3, blank=True, default=0)
    walls_mark = models.DecimalField(max_digits=6, decimal_places=3, blank=True, default=0)
    roof_mark = models.DecimalField(max_digits=6, decimal_places=3, blank=True, default=0)
    construction_reliability = models.DecimalField(max_digits=100, decimal_places=3, default=0)
    construction_damage = models.DecimalField(max_digits=100, decimal_places=3, default=0)
    final_coefficient = models.DecimalField(max_digits=100, decimal_places=3, default=0)

    def __str__(self):
        return "{}, {}".format(self.foundation_mark,
                               self.construction_reliability)


class Prediction(models.Model):
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    years_until_full_fix = models.DecimalField(max_digits=100, decimal_places=2, blank=True, default=0)
    years_until_full_warning = models.DecimalField(max_digits=100, decimal_places=2, blank=True, default=0)
    construction_damage_predicted = ArrayField(models.DecimalField(max_digits=100, decimal_places=3))

    def __str__(self):
        return "{}, {}".format(self.date,
                               self.years_until_full_fix,
                               self.years_until_full_warning)
