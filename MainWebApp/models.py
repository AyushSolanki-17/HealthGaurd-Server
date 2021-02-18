from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, Group)


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
        group = Group.objects.get(name="Patients")
        group.user_set.add(user)
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


class HealthGuardUser(AbstractBaseUser, PermissionsMixin):
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
    is_admin = models.BooleanField(default=False)

    objects = HealthGuardUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'gender', 'dob', 'mobile']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'Users'
        permissions = (
            ('view_patient_test_data', 'View patient\'s Test data'),
            ('edit_patient_test_data', 'Edit patient\'s Test data'),
        )


class HealthGuardDoctorManager(models.Manager):

    def create_doctor(self, user_email, qualification, speciality, license_pdf):
        user = HealthGuardUser.objects.get(email=user_email)
        doctor = self.model(
            user=user,
            qualification=qualification,
            speciality=speciality,
            license_pdf=license_pdf
        )
        user.groups.clear()
        group = Group.objects.get(name="Doctors")
        group.user_set.add(user)
        doctor.save(using=self._db)
        return doctor


class HealthGuardDoctor(models.Model):
    user = models.OneToOneField(
        HealthGuardUser,
        on_delete=models.CASCADE,
        verbose_name='user',
        primary_key=True
    )
    qualification = models.CharField(
        verbose_name='qualification',
        max_length=20,
    )
    speciality = models.CharField(
        verbose_name='speciality',
        max_length=255,
    )
    license_pdf = models.FileField(
        verbose_name='license_pdf',
        upload_to='license/%Y/%m/',
        blank=False,
        null=False,
    )
    is_approved = models.BooleanField(
        verbose_name='is_approved',
        default=False,
    )
    objects = HealthGuardDoctorManager()

    class Meta:
        db_table = 'Doctors'

