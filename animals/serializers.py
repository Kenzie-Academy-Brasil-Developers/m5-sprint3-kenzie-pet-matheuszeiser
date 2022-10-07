from rest_framework import serializers
from animals.exceptions import NonUpdatableKeyError

from traits.models import Trait
from groups.models import Group
from animals.models import Animal, SexOptions
from groups.serializers import GroupSerializer
from traits.serializers import TraitsSerializer


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexOptions.choices,
        default=SexOptions.DEFAULT,
    )
    group = GroupSerializer()
    traits = TraitsSerializer(many=True)
    age_in_human_years = serializers.SerializerMethodField()

    def create(self, validated_data: dict) -> Animal:
        group_data = validated_data.pop("group")
        trait_data = validated_data.pop("traits")

        group, created = Group.objects.get_or_create(**group_data)

        animal = Animal.objects.create(**validated_data, group=group)

        for trait in trait_data:
            get_trait, created = Trait.objects.get_or_create(**trait)
            animal.traits.add(get_trait)

        return animal

    def update(self, instance: Animal, validated_data: dict) -> Animal:
        for key, value in validated_data.items():
            if key == "group" or key == "traits" or key == "sex":
                msg = {f"{key}": f"You cannot update {key} property"}
                raise NonUpdatableKeyError(msg)
            setattr(instance, key, value)

        instance.save()

        return instance

    def get_age_in_human_years(self, obj: Animal):
        return obj.age_in_human_method()
