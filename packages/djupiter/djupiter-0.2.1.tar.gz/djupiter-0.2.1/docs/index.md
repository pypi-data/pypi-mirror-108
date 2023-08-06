# Djupiter

Djupter is a Django app that provides production-ready REST endpoints for common authentication flows.

Get the package: `pip install djupiter`

## Quickstart

1. Add "djupiter" and "drf_yasg" to your INSTALLED_APPS setting like this:
```python
INSTALLED_APPS = [
    ...
    "drf_yasg",
    "rest_framework.authtoken",
    "djupiter",
]
```

2. Fill out the following fields on your settings file:
```python
# Used for the auto-generated API docs
PROJECT_NAME = "My Project"
PROJECT_DEVELOPER_EMAIL = "developer@example.com"
PROJECT_API_VERSION = "0.0.1"

# Used for sending emails.
EMAIL_FROM = "no-reply@example.com"
## For production:
# EMAIL_HOST = os.environ.get("EMAIL_HOST")
# EMAIL_USE_TLS = int(os.environ.get("EMAIL_USE_TLS", default=0))
# EMAIL_PORT = os.environ.get("EMAIL_PORT")
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

## For testing:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Use the custom Djupiter User model
AUTH_USER_MODEL = 'djupiter.User'
```

3. Include the djupiter URLconf in your project urls.py like this:
```python
path('api/', include('djupiter.urls')),
```

4. Run `python manage.py migrate` to create the djupiter models.

5. Visit `http://127.0.0.1:8000/api/docs` for the API documentation. Happy hacking!