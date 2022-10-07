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
            "age": 1,
            "weight": 12,
            "sex": "Macho",
            "group": {
                "name": "Cachorro",
                "scientific_name": "Caninus",
            },
            "traits": [{"name": "Agressivo"}],
        }
        cls.group_data = cls.animal_data.pop("group")
        cls.traits_data = cls.animal_data.pop("traits")

        cls.group = Group.objects.create(**cls.group_data)

        cls.animal = Animal.objects.create(**cls.animal_data, group=cls.group)

        for trait in cls.traits_data:
            get_trait, created = Trait.objects.get_or_create(**trait)
            cls.animal.traits.add(get_trait)

    def test_animals_attr(self):
        """
        Verifica se as propriedades dos campos da model Animal estão corretas
        """
        name_max_length = self.animal._meta.get_field("name").max_length
        sex_max_length = self.animal._meta.get_field("sex").max_length

        self.assertEqual(name_max_length, 50)
        self.assertEqual(sex_max_length, 15)

    def test_animals_fields(self):
        """
        Verifica se os campos estão sendo atribuidos corretamente
        """
        self.assertEqual(self.animal_data["name"], self.animal.name)
        self.assertEqual(self.animal_data["age"], self.animal.age)
        self.assertEqual(self.animal_data["weight"], self.animal.weight)
        self.assertEqual(self.animal_data["sex"], self.animal.sex)
        self.assertEqual(self.group_data["name"], self.group.name)
        self.assertEqual(
            self.group_data["scientific_name"], self.animal.group.scientific_name
        )

    def test_convert_age_to_human_years(self):

        age_human = self.animal.age_in_human_method()

        self.assertEqual(age_human, 31)
