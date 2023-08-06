import setuptools
from setuptools import setup

setup(
    install_requires=[
        "Django>=3.1.5",
        "psycopg2-binary>=2.8.6",
        "django-cors-headers>=3.6.0",
        "djangorestframework>=3.11.2",
        "Pillow>=8.1.0",
        "factory-boy>=3.2.0", 
        "drf-yasg>=1.20.0",
        "drf-extra-fields>=3.0.4",
        "wheel",
    ]
)