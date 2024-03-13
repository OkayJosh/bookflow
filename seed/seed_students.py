from django.contrib.auth.hashers import make_password
from student.models import Student


def create_staff_students():
    for i in range(10):
        phone_number = f"123456789{i}"
        address = f"Address {i}"
        email = f"student{i}@bookflow.com"
        first_name = f"Student {i}"
        username = f"student{i}"
        last_name = f"Student Last name {i}"
        raw_password = "password"

        # Check if a user with the same username or email already exists
        if not Student.objects.filter(username=username).exists() and not Student.objects.filter(email=email).exists():
            # Hash the password
            hashed_password = make_password(raw_password)

            # Create a new student instance
            Student.objects.create(
                username=username,
                phone_number=phone_number,
                address=address,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=hashed_password,  # Save the hashed password
                is_staff=True,
                is_active=True
            )


def create_students():
    for i in range(11, 20):
        phone_number = f"123456789{i}"
        address = f"Address {i}"
        email = f"student{i}@bookflow.com"
        first_name = f"Student {i}"
        username = f"student{i}"
        last_name = f"Student Last name {i}"
        raw_password = "password"

        # Check if a user with the same username or email already exists
        if not Student.objects.filter(username=username).exists() and not Student.objects.filter(email=email).exists():
            # Hash the password
            hashed_password = make_password(raw_password)

            # Create a new student instance
            Student.objects.create(
                username=username,
                phone_number=phone_number,
                address=address,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=hashed_password,  # Save the hashed password
                is_active=True
            )
