from django.test import TestCase
from animals.models import Animal
from groups.models import Group
from traits.models import Trait
from animals.serializers import AnimalSerializer


class AnimalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.animal_data = {
            "name": "Bob",
            "age": 3,
            "weight": 12,
            "sex": "Macho",
        }

        cls.group_data_1 = {
            "name": "Cachorro",
            "scientific_name": "Caninus",
        }
        cls.group_data_2 = {
            "name": "Gato",
            "scientific_name": "Felinus",
        }

        cls.traits_data = [{"name": "Agressivo"}, {"name": "Peludo"}]

        cls.group = Group.objects.create(**cls.group_data_1)

        cls.animals = [Animal.objects.create(**cls.animal_data) for _ in range(10)]

        for trait in cls.traits_data:
            get_trait, created = Trait.objects.get_or_create(**trait)
            cls.animal.traits.add(get_trait)

    def test_group_may_contain_multiple_animals(self):
        for animal in self.animals:
            animal.group = self.group
            animal.save()

        self.assertEqual(
            len(self.animals),
            self.group.animals.count(),
        )

        for animal in self.animals:
            self.assertIs(animal.group, self.group)

    def test_animal_cannot_belong_to_more_than_one_group(self):

        for animal in self.animals:
            animal.group = self.group
            animal.save()

        group_two = Group.objects.create(**self.group_data_2)

        for animal in self.animals:
            animal.group = group_two
            animal.save()

        for animal in self.animals:
            self.assertNotIn(animal, self.group.animals.all())
            self.assertIn(animal, group_two.animals.all())
