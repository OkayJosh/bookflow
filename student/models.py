import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser


class Student(TimeStampedModel, AbstractUser):
    """
    Represents a student in the system.

    Attributes:
        student_id (UUIDField): Unique identifier for the student.
        phone_number (CharField): Contact phone number of the student.
        address (CharField): Physical address of the student.
        email (EmailField): Email address of the student.

    Meta:
        db_table (str): Specifies the database table name for the model.
        verbose_name (str): Human-readable name for a single instance of the model.
        verbose_name_plural (str): Human-readable name for the model in plural form.
    """

    student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        error_messages={
            "unique": "A user with that phone_number already exists.",
        },
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(
        unique=True,
        blank=True,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )

    class Meta:
        db_table = "Student"
        verbose_name = "Student"
        verbose_name_plural = "Students"
