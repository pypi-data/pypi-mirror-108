# Models

Usage guide in progress...

```python
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin): pass

class SuperAdmin(User): pass

class Commoner(User): pass

class PasswordResetCode(models.Model): pass

class ConfirmationCode(models.Model): pass
```