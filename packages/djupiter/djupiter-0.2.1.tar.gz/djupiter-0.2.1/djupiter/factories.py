import uuid

import factory

from djupiter.models import User, PasswordResetCode


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.Faker("phone_number")
    address = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state")
    zip = factory.Faker("postcode")
    is_email_confirmed = True


class SuperAdminFactory(UserFactory):
    is_superuser = True
    is_staff = True


class CommonerFactory(UserFactory):
    is_superuser = False
    is_staff = False


class PasswordResetCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PasswordResetCode

    code = factory.LazyFunction(lambda: uuid.uuid4().hex.upper()[:4])
    user = factory.SubFactory(UserFactory)
