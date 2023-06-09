from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import AbstractUser, BaseUserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        DIRECTOR = "DIRECTOR", 'director'
        MANAGER = "MANAGER", "manager"

    subject = models.CharField(max_length=150, verbose_name="Subject", null=True, blank=True)
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    role = models.CharField(max_length=15, choices=Role.choices, null=True, blank=True)

    class Meta:
        db_table = "User"


class DirectorManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username or len(username) <= 0:
            raise ValueError("Username field is required !")
        if not password:
            raise ValueError("Password is must !")

        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.DIRECTOR)


class ManagerManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username or len(username) <= 0:
            raise ValueError("Username field is required !")
        if not password:
            raise ValueError("Password is must !")

        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.MANAGER)


class Director(User):
    base_role = User.Role.DIRECTOR

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    objects = DirectorManager()


class Manager(User):
    base_role = User.Role.MANAGER

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    objects = ManagerManager()




class Mijoz(models.Model):
    CustomerType = (
        ('Tezkor mijoz', 'Tezkor mijoz'),
        ('Doimiy mijoz', 'Doimiy mijoz'),
    )
    customer_type = models.CharField(choices=CustomerType, max_length=223, default='Tezkor mijoz')
    ism_sharif = models.CharField(max_length=200)
    telefon = models.CharField(max_length=13, null=True, blank=True)
    vaqt = models.DateTimeField(auto_now_add=True)
    izoh = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.ism_sharif

    class Meta:
        verbose_name = 'Mijoz'
        verbose_name_plural = 'Mijozlar'



class Ishchi(models.Model):
    lavozim = models.CharField(max_length=200)
    ism_sharif = models.CharField(max_length=200)
    telefon = models.FloatField()
    vaqt = models.DateTimeField()

    def get_count(self):
        return Ishchi.objects.count()

    def __str__(self):
        return f"{self.ism_sharif} | {self.lavozim} "

    class Meta:
        verbose_name = "Ishchi"
        verbose_name_plural = "Ishchilar"

