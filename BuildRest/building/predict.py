from datetime import date
from dateutil import relativedelta as rdelta
from math import log, e, pow


def years_until_damage(wear):
    return 0.16 / wear


def years_until_warning(wear):
    return 0.22 / wear


def wear_calc(reliability, age):
    return -(log(reliability) / age)


def damage_calc(predicted_age, wear):
    return round(1 - pow(e, -(wear * predicted_age)), 3)


def prediction(id, reliability, date_build):
    age = rdelta.relativedelta(date.today(), date_build).years
    wear = wear_calc(reliability, age)
    predicted_values = []
    years_ahead = 5
    for i in range(10):
        predicted_values.append(round(damage_calc(years_ahead, wear), 3))
        years_ahead += 5

    result = {
        "years_until_full_fix": round(years_until_damage(wear), 1),
        "years_until_full_warning": round(years_until_warning(wear), 1),
        "construction_damage_predicted": predicted_values,
        "construction": id
    }

    return result
