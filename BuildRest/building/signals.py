from django.db.models.signals import post_save
from django.dispatch import receiver
from .evaluate import evaluate
from .models import Measurement, Construction, Evaluation


@receiver(post_save, sender=Measurement)
def measurement_post_post_save(sender, instance, created, **kwargs):
    if created:
        building = Construction.objects.select_related('roof', 'walls', 'floor', 'foundation').get(id=instance.construction_id)
        result = (evaluate(instance.id, building.build_date,
                           [building.roof.roof_material, building.walls.walls_material, building.floor.floor_type,
                            building.foundation.foundation_material],
                           instance.humidity, instance.acoustic_analysis, instance.vibration))
        evaluation = Evaluation(
            foundation_mark=result['foundation_mark'],
            floor_mark=result['floor_mark'],
            walls_mark=result['walls_mark'],
            roof_mark=result['roof_mark'],
            construction_reliability=result['construction_reliability'],
            construction_damage=result['construction_damage'],
            final_coefficient=result['final_coefficient'],
            measurement=instance,
        )
        evaluation.save()
