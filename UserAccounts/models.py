from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

# Create your models here.




class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username=None, password=None, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username=None, password=None, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        if username == None:
            username = email

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)

        if password is not None:
            user.set_password(password)

        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    # this fields are mandatory for all type of users
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)

    # this fields for individual user
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)

    # details
    gender = models.CharField(max_length=10, blank=True, null=True)
    gender_on_profile = models.BooleanField(default=False)
    birthdate = models.DateField(blank=True, null=True)
    interested_in_gender = models.CharField(max_length=10, blank=True, null=True)

    interests = ArrayField(models.CharField(max_length=25, blank=True), size=8, blank=True, null=True)
    looking_for = models.CharField(max_length=50, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(blank=True, null=True)

    # mandatory
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)



    # settings
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username



class otp(models.Model):
    email = models.CharField(max_length=70, blank=True, null=True)
    otp = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)






