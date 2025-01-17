"""Deals with user models in the database

OpenIDCUserManager() manages how a OpenID Connect (Aberystwyth) user is created and added to the database
OpenIDCUser() database model for OpenID Connect (Aberystwyth) users
DiscordUserOAuth2Manager() manages how a Discord user is created and added to the database
DiscordUser() database model for Discord users
"""

__author__ = "Joel Adams"
__maintainer__ = "Joel Adams"
__email__ = "joa38@aber.ac.uk"
__version__ = "2.0"
__status__ = "Production"
__system__ = "Django website"
__deprecated__ = False

from django.db import models
from django.contrib.auth import models as authModels
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class OpenIDCUserManager(BaseUserManager):
    def create_user(self, user, password=None):
        new_user = self.model(
            username = user['OIDC_CLAIM_preferred_username'],
            name = user['OIDC_CLAIM_name'],
            email = user['OIDC_CLAIM_email'],
            usertype = user['OIDC_CLAIM_usertype']
        )
        if user['OIDC_CLAIM_usertype'] == "staff":
            new_user.is_admin = True
        new_user.save(using=self._db)
        return new_user

class OpenIDCUser(AbstractBaseUser):
    objects = OpenIDCUserManager()

    class usertypes(models.TextChoices):
        STAFF = 'staff'
        UNDERGRAD = 'undergrad'
        POSTGRAD = 'postgrad'
        OFFICE = 'office'
        CONTED = 'conted'
        SUMMER = 'summer'
        WEB = 'web'
        TEMPORARY = 'temporary'
        UNKNOWN = 'unknown'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    username = models.CharField(max_length=40)
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=30)
    usertype = models.CharField(max_length=50, choices=usertypes.choices)
    last_login = models.DateTimeField(null=True)
    password = None
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['username', 'name', 'email', 'usertype']
    
    def has_perm(self, perm, obj=None):
        if self.usertype == 'staff':
            return True
        else:
            return False

    def has_module_perms(self, app_label):
        if self.usertype == 'staff':
            return True
        else:
            return False

    @property
    def is_staff(self):
        return self.is_admin
    
    def __str__(self):
        return "{} {}".format(self.__class__.__name__, self.username)

    class Meta:
        verbose_name = 'Aberystwyth user'

'''class StaffManager(models.Manager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(usertype=OpenIDCUser.usertypes.STAFF)

class UndergradManager(models.Manager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(usertype=OpenIDCUser.usertypes.UNDERGRAD)

class Staff(OpenIDCUser):
    objects = StaffManager()

    class Meta:
        proxy = True

class Undergrad(OpenIDCUser):
    objects = UndergradManager()

    class Meta:
        proxy = True'''


class DiscordUserOAuth2Manager(authModels.UserManager):

    def create_user(self, user, openidc_user):
        discord_username = '%s#%s' % (user['username'], user['discriminator']) 
        new_user = self.create(
            id=user['id'],
            last_login=timezone.now(),
            openidc=openidc_user

        )
        return new_user

class DiscordUser(models.Model):
    objects = DiscordUserOAuth2Manager()

    id = models.BigIntegerField(primary_key=True)
    last_login = models.DateTimeField(null=True)
    openidc = models.ForeignKey(OpenIDCUser, on_delete=models.CASCADE, related_name='aber_id')

    def is_authenticated(self, request):
        return True

    def is_active(self, request):
        return False

    def is_staff(self, request):
        return False

    def has_perm(self, perm):
        return False

    def has_module_perms(self, app_label):
        return False

    def __str__(self):
        return "{} {}".format(self.__class__.__name__, self.id)
