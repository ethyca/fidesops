import logging
from faker import Faker

logging.getLogger("faker").setLevel(logging.ERROR)
faker = Faker(use_weighting=False)

from faker.providers.lorem.en_US import Provider as lorem
from faker.providers import address

faker.add_provider(address)
faker.add_provider(lorem)
# for a list of bundled providers, see https://faker.readthedocs.io/en/master/providers.html


def bothify(pattern: str):
    """Replaces '?' with ascii, '#' with numbers"""
    return faker.bothify(pattern)


def full_name():
    return faker.name()


def text():
    return faker.paragraph()
