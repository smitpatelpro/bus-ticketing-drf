from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
from .managers import UserManager
from django.core.validators import MinLengthValidator
from softdelete.models import SoftDeleteObject, SoftDeleteManager

# BASE Classes
class BaseModel(SoftDeleteObject, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = (True,)


class SoftDeleteUserManager(UserManager, SoftDeleteManager):
    pass


# Models
class User(BaseModel, AbstractBaseUser):
    objects = SoftDeleteUserManager()
    ROLES = (
        ("ADMIN", "ADMIN"),
        ("BUS_OPERATOR", "BUS_OPERATOR"),
        ("CUSTOMER", "CUSTOMER"),
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, validators=[MinLengthValidator])
    role = models.CharField(choices=ROLES, max_length=20)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.full_name

    def __str__(self):
        return "{} ({})".format(self.email, self.id)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Media(BaseModel):
    file = models.FileField()

    def __str__(self) -> str:
        return "{} ({})".format(self.file, self.id)
