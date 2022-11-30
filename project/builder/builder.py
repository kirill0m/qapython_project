import dataclasses
import math
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from faker import Faker


class Builder:
    def __init__(self):
        self.fake = Faker('en_US')

    def generate_value(self, length=10, value_type=''):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        specific = "=+<>.,_'-/\[]!@#$%^&*() "

        if value_type == 'specific':
            return self.fake.bothify(length * '?', letters=specific)
        elif value_type == 'nums':
            return self.fake.numerify(length * '#')
        elif value_type == 'all':
            return self.fake.bothify(round(length/2) * '#?', letters=letters+specific)
        elif value_type == 'space':
            return length * ' '
        else:
            return self.fake.lexify(length * '?')

    def generate_email(self, length=0):
        min_domain = '@y.y'
        if length > 4:
            return self.generate_value(length - 4) + min_domain
        else:
            return self.fake.email()

    def generate_user_db(self):
        return [self.generate_value() * 5, self.generate_email()]

    def user(self, type='api', **kwargs):
        @dataclass_json
        @dataclass
        class User:
            name: str = kwargs['name'] if 'name' in kwargs else self.generate_value()
            surname: str = kwargs['surname'] if 'surname' in kwargs else self.generate_value()
            middle_name: str = kwargs['middle_name'] if 'middle_name' in kwargs else self.generate_value()
            username: str = kwargs['username'] if 'username' in kwargs else self.generate_value()
            password: str = kwargs['password'] if 'password' in kwargs else self.generate_value()
            email: str = kwargs['email'] if 'email' in kwargs else self.generate_email()

        user = User()

        if type == 'api':
            return user, dataclasses.asdict(user)
        elif type == 'db':
            return user, dataclasses.astuple(user)
