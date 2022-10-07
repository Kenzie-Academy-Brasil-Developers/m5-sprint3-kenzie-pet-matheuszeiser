from django.test import TestCase
from animals.models import Animal
from groups.models import Group


class TraitModelTest(TestCase):
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
            "traits": [{"name": "Agressivo"}, {"name": "peludo"}],
        }
        cls.group_data = cls.animal_data.pop("group")
        cls.traits_data = cls.animal_data.pop("traits")

        cls.group = Group.objects.create(**cls.group_data)

        cls.animal = Animal.objects.create(**cls.animal_data, group=cls.group)

    def test_group_attr(self):
        """
        Verifica se as propriedades dos campos da model Trait estão corretas
        """

        for index, trait in enumerate(self.animal.traits.all()):
            name_unique = trait._meta.get_field("name").unique
            name_max_length = trait._meta.get_field("name").max_length
            self.assertTrue(name_unique)
            self.assertEqual(name_max_length, 20)

            self.assertEqual(trait.name, self.traits_data[index]["name"])
