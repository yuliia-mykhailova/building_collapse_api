from dateutil import relativedelta as rdelta
from datetime import date


material = ('1', '2', '3', '4', '5', '6', '7', '8')
life_time = (30, 125, 20, 130, 150, 100, 15, 50)
alphas = (2, 3, 2, 3)


def evaluate(id, date_build, construction_data, humidity, acoustic, vibration):
    date_current = date.today()
    age = rdelta.relativedelta(date_current, date_build).years
    wear_calculated = []
    count_crucial = 0

    for part_material in construction_data:
        temp = round(age / life_time[int(part_material) - 1], 2)
        wear_calculated.append(temp)
        if temp * 100 > 70:
            count_crucial += 1

    protection = 1.0
    if count_crucial == 1:
        protection = 0.85
    elif count_crucial == 2:
        protection = 0.65
    elif count_crucial == 3:
        protection = 0.4
    elif count_crucial == 4:
        protection = 0.2
    elif count_crucial >= 5:
        protection = 0

    final_coefficient = round(float(humidity) * float(acoustic) * protection * float(vibration), 2)

    damage = map(lambda x, y: x * y, wear_calculated, alphas)
    damage = round((sum(damage) / sum(alphas)), 3)
    reliability = round((1 - damage), 3)

    result = {
        "foundation_mark": wear_calculated[3],
        "floor_mark": wear_calculated[2],
        "walls_mark": wear_calculated[1],
        "roof_mark": wear_calculated[0],
        "construction_reliability": reliability,
        "construction_damage": damage,
        "final_coefficient": final_coefficient,
        "measurement": id
    }

    return result