from django.test import TestCase
from animals.models import Animal
from groups.models import Group
from traits.models import Trait


class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.animal_data = {
            "name": "Bob",
            "age": 3,
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

    def test_group_attr(self):
        """
        Verifica se as propriedades dos campos da model Group estão corretas
        """
        name_max_length = self.group._meta.get_field("name").max_length
        scientific_name_max_length = self.group._meta.get_field(
            "scientific_name"
        ).max_length

        self.assertEqual(name_max_length, 20)
        self.assertEqual(scientific_name_max_length, 50)

        name_unique = self.group._meta.get_field("name").unique
        scientific_name_unique = self.group._meta.get_field("scientific_name").unique

        self.assertTrue(name_unique)
        self.assertTrue(scientific_name_unique)
