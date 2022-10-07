import math
from django.db import models
from traitlets import default


class SexOptions(models.TextChoices):
    MALE = "Macho"
    FEMALE = "Fêmea"
    DEFAULT = "Não informado"


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=15,
        choices=SexOptions.choices,
        default=SexOptions.DEFAULT,
    )

    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="animals",
        null=True,
        default=None,
    )

    traits = models.ManyToManyField(
        "traits.Trait",
        related_name="animals",
        null=True,
        default=None,
    )

    def age_in_human_method(self):
        age = round((16 * math.log10(self.age) + 31), 2)
        return age
