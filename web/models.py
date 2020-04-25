from django.db import models
#from django.conf import settings as conf_settings
from django.utils import timezone
from django.core.mail import send_mail
#from django.core.exceptions import ValidationError
#from django.core.validators import RegexValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
#from django.utils.translation import gettext_lazy as _, activate
#from django.utils.timezone import make_aware, utc
from django.utils.text import Truncator


class ProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Вкажіть e-mail')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', Profile.CUSTOMER)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['role'] = Profile.ADMIN
        return self._create_user(email, password, **extra_fields)


class Profile(AbstractBaseUser):
    # User profile with additional information
    ADMIN = 'A'
    STUDENT = 'S'
    MENTOR = 'M'
    EMPLOYER = 'E'
    ROLE_CHOICES = (
        (ADMIN, 'Адміністратор'),
        (STUDENT, 'Студент'),
        (MENTOR, 'Ментор'),
        (EMPLOYER, 'Роботодавець'),
    )

    email = models.EmailField('E-mail', unique=True)
    first_name = models.CharField('Ім\'я', max_length=32)
    last_name = models.CharField('Прізвище', max_length=32)
    is_active = models.BooleanField('Активний', default=True)
    date_joined = models.DateTimeField('Приєднався', default=timezone.now)

    # Some additional User data
    role = models.CharField('Роль', max_length=1, choices=ROLE_CHOICES, default=STUDENT)
    city = models.CharField('Місто', max_length=64)
    company = models.CharField('Компанія або навчальний заклад', max_length=255, null=True, blank=True)
    scope = models.CharField('Сфера діяльності або факультет', max_length=255, null=True, blank=True)
    course = models.PositiveIntegerField('Курс', null=True, blank=True)


    objects = ProfileManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    # Take care about compatibility :(
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        return self.role == self.ADMIN

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Opportunity(models.Model):
    employer = models.ForeignKey(Profile, on_delete=models.PROTECT,
        related_name='opportunities', verbose_name='Хто надає')
    name = models.CharField('Назва', max_length=128)
    descr = models.TextField('Опис')
    cost = models.IntegerField('Вартість', default=0)

    class Meta:
        verbose_name = 'Можливість'
        verbose_name_plural = 'Можливості'

    def short_descr(self):
        return Truncator(self.descr).words(10)
    short_descr.short_description = 'Опис'

    def __str__(self):
        return self.name
