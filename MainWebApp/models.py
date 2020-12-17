from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class HealthGuardUserManager(BaseUserManager):
    def create_user(self, email, fname, mobile, gender, dob, password=None):
        """
        Creates and saves a User with the given data
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            fname=fname,
            mobile=mobile,
            gender=gender,
            dob=dob
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fname, mobile, gender, dob, password=None):
        """
        Creates and saves a superuser with the given data
        """
        user = self.create_user(
            email,
            password=password,
            fname=fname,
            mobile=mobile,
            gender=gender,
            dob=dob
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class HealthGuardUser(AbstractBaseUser):
    GenderChoices = (('M', 'Male'), ('F', 'Female'))
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        primary_key=True,
        unique=True,
    )
    fname = models.CharField(
        verbose_name='full name',
        max_length=50
    )
    mobile = models.CharField(
        verbose_name='mobile number',
        max_length=10,
        unique=True
    )
    gender = models.CharField(
        verbose_name='gender',
        max_length=1,
        choices=GenderChoices
    )
    dob = models.DateField()
    is_doctor = models.BooleanField(default=False)
    is_chemist = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = HealthGuardUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'gender', 'dob', 'mobile']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'Users'


