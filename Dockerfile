# Use the official Python image as a base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE Bookflow.settings

# Set the working directory in the container
WORKDIR /bookflow

# Copy the current directory contents into the container at /bookflow
COPY . /bookflow

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir psycopg2-binary

# Change permissions for staticfiles directory
RUN chmod -R 775 /bookflow/staticfiles

# Run entrypoint script
CMD ["/bookflow/entrypoint.sh"]
