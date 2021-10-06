from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime,timedelta
import jwt
from django.conf import settings
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            phone=phone,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Role(models.Model):
    role=models.CharField(unique=True,max_length=255,default="user")
    def __str__(self):
        return self.role
class City(models.Model):
    city=models.CharField(unique=True,max_length=100,default="Москва")
    def __str__(self):
        return self.city
class Metro(models.Model):
    station=models.CharField(unique=True,max_length=100)
    city=models.ForeignKey(City,to_field='city',on_delete=models.CASCADE)
    def __str__(self):
        return self.station
class Location(models.Model):
    city=models.ForeignKey(City,to_field='city',on_delete=models.CASCADE)
    metro=models.ForeignKey(Metro,to_field='station',on_delete=models.CASCADE,null=True,default=None)
    street=models.CharField(max_length=255,null=True,default=None)
    house=models.IntegerField(null=True,default=None)
class User(AbstractBaseUser):
    phone=models.BigIntegerField(unique=True)
    role=models.ForeignKey(Role,to_field='role',on_delete=models.CASCADE,null=True,default=None)
    confirmed=models.BooleanField(default=False)
    subscribed=models.BooleanField(default=False)
    location=models.ForeignKey(Location,on_delete=models.RESTRICT,null=True,default=None)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()
    REQUIRED_FIELDS = ['phone']
    def __str__(self):
        return self.email

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
        # Simplest possible answer: All admins are staff
        return self.is_admin
    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()
    def _generate_jwt_token(self):
    	"""
    	Generates a JSON Web Token that stores this user's ID and has an expiry
    	date set to 60 days into the future.
    	"""
    	dt = datetime.now() + timedelta(days=60)

    	token = jwt.encode({
    	    'id': self.pk,
    	    'exp': int(dt.strftime('%s'))
    	}, settings.SECRET_KEY, algorithm='HS256')
    	return token
