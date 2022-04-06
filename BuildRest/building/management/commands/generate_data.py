import random
from django.core.management import BaseCommand
from faker import Faker
from ...models import CustomUser, Construction, Roof, Foundation, Walls, Measurement, Evaluation, Prediction, Floor
from ...predict import *


fake = Faker()


def get_user():
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = 'user12345678'
    phone = fake.phone_number()
    user = CustomUser(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone
    )
    user.set_password(password)
    user.save()
    return user


def get_construction(users):
    name = fake.word()
    address = fake.street_address()
    construction_type = random.randint(1, 3)
    height = random.randint(100, 9999)
    floor_number = random.randint(1, 10)
    build_date = fake.date()
    total_area = random.randint(100, 9999)
    owner = users[random.randint(0, len(users) - 1)]

    construction = Construction(
        name=name,
        address=address,
        construction_type=construction_type,
        height=height,
        floor_number=floor_number,
        build_date=build_date,
        total_area=total_area,
        owner=owner
    )
    construction.save()
    return construction


def get_foundation(construct):
    foundation_type = random.randint(1, 6)
    foundation_material = random.randint(1, 8)
    area = random.randint(100, 9999)
    construction = construct
    foundation = Foundation(
        construction=construction,
        area=area,
        foundation_type=foundation_type,
        foundation_material=foundation_material
    )
    foundation.save()


def get_floor(construct):
    floor_type = random.randint(1, 8)
    construction = construct
    floor = Floor(
        construction=construction,
        floor_type=floor_type
    )
    floor.save()


def get_walls(construct):
    walls_material = random.randint(1, 8)
    thickness = random.randint(100, 999)
    construction = construct
    walls = Walls(
        walls_material=walls_material,
        thickness=thickness,
        construction=construction
    )
    walls.save()


def get_roof(construct):
    roof_type = random.randint(1, 11)
    roof_material = random.randint(1, 8)
    construction = construct
    roof = Roof(
        construction=construction,
        roof_type=roof_type,
        roof_material=roof_material
    )
    roof.save()


def get_measurement(construct):
    date = fake.date()
    temperature = random.randint(0, 40)
    humidity = round(random.uniform(0, 1), 2)
    acoustic_analysis = round(random.uniform(0, 1), 2)
    vibration = round(random.uniform(0, 1), 2)
    construction = construct
    measurement = Measurement(
        construction=construction,
        date=date,
        temperature=temperature,
        humidity=humidity,
        acoustic_analysis=acoustic_analysis,
        vibration=vibration,
    )
    measurement.save()
    return measurement


def get_prediction(construct, measurement):
    date = fake.date()
    construction = construct
    evaluation_data = Evaluation.objects.get(measurement_id=measurement.id)
    build_date = Construction.objects.get(id=construct.id)
    result = prediction(construction, evaluation_data.final_coefficient, build_date.build_date)
    prediction_res = Prediction(
        construction=construction,
        date=date,
        years_until_full_fix=result['years_until_full_fix'],
        years_until_full_warning=result['years_until_full_warning'],
        construction_damage_predicted=result['construction_damage_predicted'],
    )
    prediction_res.save()


class Command(BaseCommand):
    help = 'Generates users, constructions, evaluations and predictions with test data'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', nargs='+', type=int)
        parser.add_argument('-c', '--constructions', nargs='+', type=int)
        parser.add_argument('-e', '--evaluations', nargs='+', type=int)

    def handle(self, *args, **options):
        users = []
        constructions = []
        for i in range(options['users'][0]):
            users.append(get_user())
        for i in range(options['constructions'][0]):
            constructions.append(get_construction(users))
        for construction in constructions:
            get_roof(construction)
            get_walls(construction)
            get_floor(construction)
            get_foundation(construction)
            for i in range(options['evaluations'][0]):
                measurement = get_measurement(construction)
                if random.randint(0, 1):
                    get_prediction(construction, measurement)
