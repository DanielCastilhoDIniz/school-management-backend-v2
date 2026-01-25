from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

from apps.common.models import Base


class UserManager(UserManager):

    def create_user(self, email, password=None, **extra_fields):
        """"
        Create and save a User with the given email and password"""
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password
        """
        extra_fields.pop('username', None)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active= True.')

        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')
        extra_fields.setdefault('tax_id', '00000000000')
        extra_fields.setdefault('date_of_birth', '1900-01-01')

        return self.create_user(email, password, **extra_fields)


class User(Base, AbstractUser):
    """
    Custom user model.
    Email and password are required. Other fields are optional.
    """
    username = None
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name=_('Email'),
        help_text=_("User's email address"),
        error_messages={
            'unique': _("A user with this email already exists")
        },
    )
    tax_id = models.CharField(
        unique=True,
        max_length=14,
        verbose_name=_('Tax iD'),
        help_text=_(
            'User tax identification number, e.g CPF, CIN, CNPJ, etc.'
            ),
    )
    date_of_birth = models.DateField(
        help_text=_("User's date of birth"),
        verbose_name=_("Date of birth"),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'tax_id',
        'date_of_birth',
    ]

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        indexes = [
            models.Index(fields=["tax_id"]),
            models.Index(fields=["email"]),
            models.Index(fields=["date_of_birth"]),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Retorna o nome completo do usuário."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Retorna o primeiro nome do usuário."""
        return self.first_name

    def get_email(self):
        """Retorna o email do usuário."""
        return self.email


