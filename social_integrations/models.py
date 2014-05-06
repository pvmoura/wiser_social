from django.db import models
from django.contrib import admin

def BcryptMixin(rounds=10):
    """
    Class factory that returns an abstract Django model mixin that adds tools
    to set and check bcrypt-secured passwords on user models.

    :param rounds: the number of log rounds to use for the salt generator
    :type rounds: int
    """

    class inner(models.Model):
        password = models.CharField(max_length=60)
        """ Salted bcrypt passwords are never longer than 60 characters """

        class Meta():
            abstract = True

        def set_password(self, raw_password):
            """
            Set the password of the user to `raw_password`.

            :param raw_password: text password
            :type raw_password: str
            """
            password = bcrypt.hashpw(raw_password, bcrypt.gensalt(rounds))
            self.password = password
            return True

        def check_password(self, raw_password):
            """
            Check that the user's password matches the given string.

            :param raw_password: text string
            :type raw_password: str
            """
            provided_password = bcrypt.hashpw(raw_password, self.password)
            return provided_password == self.password

        def is_authenticated(self):
            """ Instantiated users with the BcryptMixin are always authenticated """
            return True

        @property
        def is_staff(self):
            return False

        @property
        def is_active(self):
            return True

        @property
        def is_superuser(self):
            return False

    return inner

class User(models.Model, BcryptMixin()):
  name = models.CharField(max_length=64)
  username = models.CharField(max_length=254, blank=True, default="")
  email = models.EmailField(unique=True, null=True, default=None)
  biography = models.TextField(blank=True)
  version = models.IntegerField(default=2, null=False, blank=False)
  first_login = models.BooleanField(default=True)
  first_login_datetime = models.DateTimeField(default=timezone.make_aware(datetime.utcfromtimestamp(0), utc))
  last_login = models.DateTimeField(default=timezone.make_aware(datetime.utcfromtimestamp(0), utc))
  linkedin_token = models.CharField(max_length=256, blank=True, default="")


