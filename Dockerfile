# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container at /app
COPY . /app/

# Install any needed packages (if your project requires additional system packages)
# RUN apt-get update && apt-get install -y <package_name>

# Install any needed Python packages (using pip or pipenv)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Django app will run on (customize as needed)
EXPOSE 8000

# Run any additional setup commands (e.g., migrations or collectstatic)
RUN python manage.py makemigrations
RUN python manage.py migrate

# Start the Django development server (customize as needed)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
