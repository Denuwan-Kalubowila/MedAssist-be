from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_doctor', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email


class Image(models.Model):
    image = models.ImageField(upload_to='post_images')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.image


class Pdf(models.Model):
    pdf_file = models.FileField(upload_to='post_pdfs')  # Change from ImageField to FileField
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.pdf_file)


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10)
    specialties = models.CharField(max_length=15)
    about = models.CharField(max_length=45)
    time = models.CharField(max_length=20)
    experience = models.CharField(max_length=5)

    def __str__(self):
        return self.email
    
class Message(models.Model):
    message = models.TextField()
    def __str__(self):
        return self.message
